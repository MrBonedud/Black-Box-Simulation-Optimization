import random

# ----------------------------
# Signal phase identifiers
# ----------------------------
PHASE_NS = "NS_GREEN"     # North–South vehicles can move
PHASE_L1 = "LOST_1"       # Clearance / all-red
PHASE_EW = "EW_GREEN"     # East–West vehicles can move
PHASE_L2 = "LOST_2"       # Clearance / all-red
PHASE_PED = "PED"         # Pedestrian-only phase


class SimulationEngine:
    """
    Pure simulation engine.

    - Discrete-time (1 second per step)
    - Contains NO rendering or pygame code
    - Treated as a black box by optimization routines
    """

    def __init__(self, plan, p_ns, p_ew, p_ped):
        # ----------------------------
        # Queue state (vehicles waiting)
        # ----------------------------
        self.q_ns = 0  # number of NS vehicles in queue
        self.q_ew = 0  # number of EW vehicles in queue

        # ----------------------------
        # Queue state (pedestrians waiting to cross)
        # ----------------------------
        self.p_queue = 0
        self.p_ped = p_ped
        self.ped_delay = 0



        # ----------------------------
        # Arrival process parameters
        # ----------------------------
        self.p_ns = p_ns  # probability of NS arrival per second
        self.p_ew = p_ew  # probability of EW arrival per second

        # ----------------------------
        # Performance metric
        # ----------------------------
        self.total_delay = 0  # cumulative vehicle delay (queue-time)

        # ----------------------------
        # Global simulation clock
        # ----------------------------
        self.t = 0  # time in seconds

        # ----------------------------
        # Signal timing plan
        # ----------------------------
        self.plan = plan

        # Fixed phase cycle: (phase_name, duration_in_seconds)
        self.cycle = [
            (PHASE_NS, plan["ns_green"]),
            (PHASE_L1, plan["lost"]),
            (PHASE_EW, plan["ew_green"]),
            (PHASE_L2, plan["lost"]),
            (PHASE_PED, plan["ped"]),
        ]

        # Start at the first phase in the cycle
        self.cycle_idx = 0
        self.phase, self.phase_time_left = self.cycle[0]

    def step(self):
        """
        Advance the simulation by exactly 1 second.
        """
        # Advance global clock
        self.t += 1
        self.phase_time_left -= 1

        # ----------------------------
        # Vehicle arrivals (Bernoulli)
        # ----------------------------
        if random.random() < self.p_ns:
            self.q_ns += 1

        if random.random() < self.p_ew:
            self.q_ew += 1

        # ----------------------------
        # Pedestrian arrivals (Bernoulli)
        # ----------------------------
        if random.random() < self.p_ped:
            self.p_queue += 1

        # ----------------------------
        # Vehicle delay accumulation
        # ----------------------------
        self.total_delay += self.q_ns + self.q_ew
        
        # ----------------------------
        # Pedestrian delay accumulation
        # ----------------------------
        self.ped_delay += self.p_queue

        # ----------------------------
        # Vehicle service (departures)
        # ----------------------------
        if self.phase == PHASE_NS and self.q_ns > 0:
            self.q_ns -= 1

        if self.phase == PHASE_EW and self.q_ew > 0:
            self.q_ew -= 1

        # ----------------------------
        # Pedestrian service (serve-all)
        # ----------------------------
        if self.phase == PHASE_PED:
            self.p_queue = 0

        # ----------------------------
        # Phase transition logic
        # ----------------------------
        if self.phase_time_left == 0:
            self.cycle_idx = (self.cycle_idx + 1) % len(self.cycle)
            self.phase, duration = self.cycle[self.cycle_idx]
            self.phase_time_left = duration

        return self.snapshot()

    def snapshot(self):
        """
        Return a read-only view of the current system state.

        This is the ONLY interface exposed to:
        - visualization
        - performance evaluation
        - optimization routines
        """
        return {
            "t": self.t,
            "phase": self.phase,
            "phase_time_left": self.phase_time_left,

            # Vehicle queues
            "q_ns": self.q_ns,
            "q_ew": self.q_ew,
            "total_delay": self.total_delay,
        
            # Pedestrian state
            "p_queue": self.p_queue,
            "ped_delay": self.ped_delay,
        }
