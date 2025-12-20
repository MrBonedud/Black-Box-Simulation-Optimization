import random
from engine import SimulationEngine
from statistics import mean

def run_single(plan, p_ns, p_ew, p_ped, T, seed):
    random.seed(seed)
    engine = SimulationEngine(plan, p_ns, p_ew, p_ped)

    for _ in range(T):
        engine.step()

    veh_delay = engine.total_delay / T
    ped_delay = engine.ped_delay / T

    return veh_delay, ped_delay

def evaluate(plan, p_ns, p_ew, p_ped, T, N):
    veh = []
    ped = []

    for i in range(N):
        v, p = run_single(plan, p_ns, p_ew, p_ped, T, seed=i)
        veh.append(v)
        ped.append(p)

    return mean(veh), mean(ped)
