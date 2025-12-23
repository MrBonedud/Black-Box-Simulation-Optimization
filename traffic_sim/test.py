from evaluate import evaluate
import matplotlib.pyplot as plt

# -------------------------
# Fixed simulation parameters
# -------------------------
p_ns = 0.3
p_ew = 0.3
p_ped = 0.2

T = 1800
N = 20
LOST_TIME = 3

# -------------------------
# Generate ~100 distinct policies
# -------------------------
ped_times = range(5, 30, 3)       # pedestrian times
ns_greens = range(10, 31, 5)      # NS green times
ew_greens = range(10, 31, 5)      # EW green times

results = []

for ped_time in ped_times:
    for ns_green in ns_greens:
        for ew_green in ew_greens:

            plan = {
                "ns_green": ns_green,
                "ew_green": ew_green,
                "lost": LOST_TIME,
                "ped": ped_time,
            }

            veh_delay, ped_delay = evaluate(
                plan,
                p_ns,
                p_ew,
                p_ped,
                T,
                N
            )

            results.append({
                "veh": veh_delay,
                "ped": ped_delay,
                "ped_time": ped_time,
                "ns": ns_green,
                "ew": ew_green
            })

            print(
                f"NS={ns_green:2d} EW={ew_green:2d} PED={ped_time:2d} | "
                f"Vehicle={veh_delay:7.2f} Ped={ped_delay:7.2f}"
            )

# -------------------------
# Prepare plotting data
# -------------------------
veh_vals = [r["veh"] for r in results]
ped_vals = [r["ped"] for r in results]
ped_times_plot = [r["ped_time"] for r in results]

min_vehicle_idx = min(range(len(results)), key=lambda i: veh_vals[i])
min_ped_idx = min(range(len(results)), key=lambda i: ped_vals[i])

# -------------------------
# Plot trade-off
# -------------------------
plt.figure(figsize=(9, 7))

scatter = plt.scatter(
    veh_vals,
    ped_vals,
    c=ped_times_plot,
    cmap="viridis",
    alpha=0.75,
    edgecolors="k",
    linewidths=0.3
)

plt.scatter(
    veh_vals[min_vehicle_idx],
    ped_vals[min_vehicle_idx],
    color="red",
    s=120,
    marker="X",
    label="Min Vehicle Delay"
)

plt.scatter(
    veh_vals[min_ped_idx],
    ped_vals[min_ped_idx],
    color="orange",
    s=120,
    marker="D",
    label="Min Pedestrian Delay"
)

plt.xlabel("Average Vehicle Delay")
plt.ylabel("Average Pedestrian Delay")
plt.title("Vehicle–Pedestrian Delay Trade-off\n(~100 Black-Box Simulation Experiments)")

cbar = plt.colorbar(scatter)
cbar.set_label("Pedestrian Phase Duration (seconds)")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
