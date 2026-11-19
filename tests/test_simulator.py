import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "simulator"))
from signals import make_fleet, next_reading  # noqa: E402

T0 = 1_763_400_000_000


def test_same_seed_gives_same_fleet():
    a = make_fleet(50, 3, seed=1)
    b = make_fleet(50, 3, seed=1)
    assert [s.base_temp_c for s in a] == [s.base_temp_c for s in b]
    assert {s.site for s in a} == {"plant-01", "plant-02", "plant-03"}


def test_seq_counts_up():
    rng = random.Random(0)
    s = make_fleet(1)[0]
    seqs = [next_reading(s, T0 + i, rng)["seq"] for i in range(5)]
    assert seqs == [1, 2, 3, 4, 5]


def test_fault_reaches_critical_vibration():
    rng = random.Random(0)
    s = make_fleet(1)[0]
    s.faulting = True  # force a fault
    vibs = [next_reading(s, T0 + i, rng, fault_rate=0)["vibration_mm_s"] for i in range(400)]
    assert max(vibs) >= 4.5