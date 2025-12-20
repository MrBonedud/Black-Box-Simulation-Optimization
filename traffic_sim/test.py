from evaluate import evaluate
import matplotlib.pyplot as plt

p_ns = 0.3
p_ew = 0.3
p_ped = 0.2

T = 1800
N = 20

results = []

for ped_time in [5, 8, 10, 12, 15, 20]:
    plan = {
        "ns_green": 20,
        "ew_green": 20,
        "lost": 3,
        "ped": ped_time,
    }

    v, p = evaluate(plan, p_ns, p_ew, p_ped, T, N)
    results.append((v, p))

    print(f"PED={ped_time:2d}  Vehicle={v:.2f}  Ped={p:.2f}")


veh = [r[0] for r in results]
ped = [r[1] for r in results]

plt.figure()
plt.scatter(veh, ped)

plt.xlabel("Average Vehicle Delay")
plt.ylabel("Average Pedestrian Delay")
plt.title("Vehicle Pedestrian Delay Trade-off (Pareto Front)")

plt.grid(True)
plt.show()
