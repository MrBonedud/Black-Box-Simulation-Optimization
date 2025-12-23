# Traffic Signal Optimization Simulation

A discrete-time simulation framework for optimizing traffic signal timing at an intersection, balancing vehicle and pedestrian delays.

## Overview

This project simulates a 4-way intersection with:

- **North–South (NS)** traffic
- **East–West (EW)** traffic
- **Pedestrian crossing** phases

The simulator evaluates different signal timing plans and generates a trade-off analysis between minimizing vehicle delay and pedestrian delay.

## Project Structure

### Core Files

- **`engine.py`** — `SimulationEngine` class

  - Pure simulation engine (no UI dependencies)
  - Discrete-time stepping (1 second per step)
  - Manages vehicle queues, pedestrian queues, and signal phases
  - Returns system state snapshots for visualization/evaluation

- **`evaluate.py`** — Evaluation utilities

  - `run_single()`: Runs one deterministic simulation with a given seed
  - `evaluate()`: Runs multiple replications of a signal plan and returns average delays
  - Uses Monte Carlo averaging over N independent runs

- **`test.py`** — Parameter sweep and trade-off analysis

  - Tests ~100 different signal timing plans
  - Generates a scatter plot showing vehicle vs. pedestrian delay trade-off
  - Identifies optimal policies for each objective

- **`main.py`** — Real-time pygame visualization
  - Live 2D rendering of the intersection
  - Shows queue lengths as bar charts
  - Displays current signal phase and time remaining

## How It Works

### Signal Cycle

Each cycle consists of 5 phases (configurable duration):

1. **NS_GREEN** — North–South vehicles move
2. **LOST_1** — All-red clearance interval
3. **EW_GREEN** — East–West vehicles move
4. **LOST_2** — All-red clearance interval
5. **PED** — Pedestrian crossing phase

### Arrival Process

Arrivals follow a Bernoulli process:

- Each second, NS vehicles arrive with probability `p_ns`
- Each second, EW vehicles arrive with probability `p_ew`
- Each second, pedestrians arrive with probability `p_ped`

### Performance Metrics

- **Vehicle Delay**: Sum of all vehicles' waiting times, averaged over time
- **Pedestrian Delay**: Sum of all pedestrians' waiting times, averaged over time

## Usage

### Run the Real-Time Visualization

```bash
python traffic_sim/main.py
```

Displays a live 2D view of the intersection with queue lengths and signal status.

### Run Parameter Sweep & Trade-off Analysis

```bash
python traffic_sim/test.py
```

Tests 100 signal timing plans and shows a scatter plot of the vehicle–pedestrian delay trade-off.

### Evaluate a Single Plan Programmatically

```python
from traffic_sim.evaluate import evaluate

plan = {
    "ns_green": 20,
    "ew_green": 20,
    "lost": 3,
    "ped": 10,
}

veh_delay, ped_delay = evaluate(plan, p_ns=0.3, p_ew=0.3, p_ped=0.2, T=1800, N=20)
print(f"Vehicle Delay: {veh_delay:.2f}, Pedestrian Delay: {ped_delay:.2f}")
```

## Parameters

### Signal Plan (`plan` dictionary)

- `ns_green` — Duration of NS green phase (seconds)
- `ew_green` — Duration of EW green phase (seconds)
- `lost` — Duration of each all-red clearance phase (seconds)
- `ped` — Duration of pedestrian crossing phase (seconds)

### Simulation Settings

- `p_ns` — Probability of NS vehicle arrival per second (0–1)
- `p_ew` — Probability of EW vehicle arrival per second (0–1)
- `p_ped` — Probability of pedestrian arrival per second (0–1)
- `T` — Simulation horizon (seconds)
- `N` — Number of independent replications for averaging

## Dependencies

- `random` — Python standard library (for stochastic arrivals)
- `matplotlib` — Plotting (for trade-off visualization)
- `pygame` — Real-time graphics (for live visualization in `main.py`)

## Example Output

Running `test.py` produces a scatter plot showing:

- **X-axis**: Average vehicle delay
- **Y-axis**: Average pedestrian delay
- **Color**: Pedestrian phase duration
- **Red X**: Policy minimizing vehicle delay
- **Orange Diamond**: Policy minimizing pedestrian delay
