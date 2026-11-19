"""Realistic vibration and temperature readings for a fleet of motors."""

import math
import random
from dataclasses import dataclass

# the motors workload rises and falls every 10 minutes
LOAD_PERIOD_S = 600.0

@dataclass
class Sensor:
    sensor_id: str 
    site: str 
    base_temp_c: float # this motor's normal temperature
    base_vib_mm_s: float # this motor's normal vibration
    phase: float # so motors aren't all in sync
    seq: int = 0 # how many readings this motor has sent
    fault: float = 0.0 # 0 = healthy, 1 = badly damaged
    faulting: bool = False # is a fault currently developing?

def make_fleet(n: int, n_sites: int = 3, seed: int = 42) -> list [Sensor]:
        """Create n motors spread across n_sites faactories."""
        rng = random.Random(seed) #same seed = same fleet every run
        sites = [f"plant-{i + 1:02d}" for i in range(n_sites)]
        fleet = []
        for i in range(n):
            fleet.append(
                Sensor(
                    sensor_id=f"motor-{i + 1:04d}",
                    site=sites[i % n_sites],
                    base_temp_c=rng.uniform(38.0, 55.0),
                    base_vib_mm_s=rng.uniform(0.6, 1.6),
                    phase=rng.uniform(0, 2 * math.pi),
                )
            )        
        return fleet

def next_reading(s: Sensor, now_ms: int, rng: random.Random, fault_rate: float = 0.0005) -> dict:
    """Produce this motor's next reading as a dict."""
    s.seq += 1
    t = now_ms / 1000.0
    load = 0.5 + 0.5 * math.sin(2 * math.pi + t / LOAD_PERIOD_S + s.phase) # between 0 and 1

    # Occasionally a bearing starts to fall, then gets steadily worse.
    if not s.faulting and rng.random() < fault_rate:
        s.faulting = True
    if s.faulting: 
        s.fault = min(1.0, s.fault + rng.uniform(0.004, 0.02))
        if s.fault >= 1.0 and rng.random() < 0.02: # a maintenance crew fixes it
            s.faulting, s.fault = False, 0.0

    temp = s.base_temp_c + 8.0 * load +30.0 * s.fault + rng.gauss(0, 0.4)
    vib = s.base_vib_mm_s * (0.8 + 0.4 * load) + 6.0 * s.fault **2 + abs(rng.gauss (0, 0.08))
                                                                
    return {
        "schema": 1,
        "sensor_id": s.sensor_id,
        "site": s.site,
        "ts": now_ms,
        "seq": s.seq,
        "temperature_c": round(temp, 2),
        "vibration_mm_s": round(vib, 3),
    }