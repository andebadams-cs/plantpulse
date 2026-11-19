#!/usr/bin/env python3
"""PlantPulse sensor fleet simulator.

Example:
  python simulator/simulate.py --sensors 5 --interval 1 --duration 5 --dry-run
"""

import argparse
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # so "import signals" works
from signals import make_fleet, next_reading  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description="PlantPulse sensor simulator")
    p.add_argument("--sensors", type=int, default=50, help="number of motors")
    p.add_argument("--sites", type=int, default=3, help="number of factories")
    p.add_argument("--interval", type=float, default=5.0, help="seconds between readings per motor")
    p.add_argument("--duration", type=float, default=0, help="seconds to run (0 = until Ctrl+C)")
    p.add_argument("--fault-rate", type=float, default=0.0005)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--dry-run", action="store_true", help="print readings instead of sending them")
    args = p.parse_args()

    rng = random.Random(args.seed)
    fleet = make_fleet(args.sensors, args.sites, args.seed)

    # Give each motor its own start time, spread evenly across one interval,
    # so 500 motors don't all send in the same millisecond.
    start = time.monotonic()
    due = [start + args.interval * i / args.sensors for i in range(args.sensors)]

    sent = 0
    try:
        while True:
            now = time.monotonic()
            if args.duration and now - start >= args.duration:
                break
            for i, sensor in enumerate(fleet):
                if due[i] > now:
                    continue
                due[i] += args.interval
                reading = next_reading(sensor, int(time.time() * 1000), rng, args.fault_rate)
                print(json.dumps(reading, separators=(",", ":")))
                sent += 1
            time.sleep(min(0.5, max(0.0, min(due) - time.monotonic())))
    except KeyboardInterrupt:
        pass  # Ctrl+C stops it cleanly

    print(f"done: {sent} readings", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())