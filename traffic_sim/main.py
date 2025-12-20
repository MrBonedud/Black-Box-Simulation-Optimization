import pygame
from engine import SimulationEngine

# ----------------------------
# Constants
# ----------------------------
ROAD_COLOR = (70, 70, 70)
ROAD_THICKNESS = 120

RED = (200, 60, 60)
GREEN = (60, 200, 60)
GRAY = (180, 180, 180)

QUEUE_COLOR = (100, 180, 240)
TEXT_COLOR = (230, 230, 230)

WIDTH, HEIGHT = 800, 600

# ----------------------------
# Pygame initialization
# ----------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Signal Simulation")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

# ----------------------------
# Fixed signal timing plan
# ----------------------------
plan = {
    "ns_green": 20,
    "ew_green": 20,
    "lost": 3,
    "ped": 10,
}

# ----------------------------
# Create simulation engine
# ----------------------------
engine = SimulationEngine(
    plan,
    p_ns=0.3,
    p_ew=0.3,
    p_ped=0.2
)

state = engine.snapshot()

# ----------------------------
# Main loop
# ----------------------------
running = True
accum = 0.0  # real-time accumulator

while running:
    # ---- timing ----
    dt = clock.tick(60) / 1000.0
    accum += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---- advance simulation (1 sec steps) ----
    if accum >= 1.0:
        accum -= 1.0
        state = engine.step()

    # ---- derive signal colors ----
    ns_color = RED
    ew_color = RED
    ped_color = RED

    if state["phase"] == "NS_GREEN":
        ns_color = GREEN
    elif state["phase"] == "EW_GREEN":
        ew_color = GREEN
    elif state["phase"] == "PED":
        ped_color = GREEN

    # ----------------------------
    # Rendering
    # ----------------------------
    screen.fill((30, 30, 30))

    cx, cy = WIDTH // 2, HEIGHT // 2

    # Roads
    pygame.draw.rect(
        screen,
        ROAD_COLOR,
        pygame.Rect(cx - ROAD_THICKNESS // 2, 0, ROAD_THICKNESS, HEIGHT)
    )
    pygame.draw.rect(
        screen,
        ROAD_COLOR,
        pygame.Rect(0, cy - ROAD_THICKNESS // 2, WIDTH, ROAD_THICKNESS)
    )

    # ----------------------------
    # NS queue bar (vertical)
    # ----------------------------
    scale = 10
    ns_height = state["q_ns"] * scale
    base_y = HEIGHT - 40
    ns_x = cx - ROAD_THICKNESS // 2 - 30

    pygame.draw.rect(
        screen,
        QUEUE_COLOR,
        pygame.Rect(
            ns_x,
            base_y - ns_height,
            20,
            ns_height
        )
    )

    # ----------------------------
    # EW queue bar (horizontal)
    # ----------------------------
    ew_width = state["q_ew"] * scale
    base_x = 40
    ew_y = cy + ROAD_THICKNESS // 2 + 10

    pygame.draw.rect(
        screen,
        QUEUE_COLOR,
        pygame.Rect(
            base_x,
            ew_y,
            ew_width,
            10
        )
    )

    # ----------------------------
    # Signal status panel
    # ----------------------------
    panel_x = 600
    panel_y = 80
    row_spacing = 45
    circle_offset = 100
    radius = 12

    labels = ["NS", "EW", "PED"]
    colors = [ns_color, ew_color, ped_color]

    for i, label_text in enumerate(labels):
        y = panel_y + i * row_spacing

        label = font.render(label_text, True, TEXT_COLOR)
        screen.blit(label, (panel_x, y))

        pygame.draw.circle(
            screen,
            colors[i],
            (panel_x + circle_offset, y + label.get_height() // 2),
            radius
        )

    # ----------------------------
    # Text displays
    # ----------------------------
    phase_text = big_font.render(
        f"{state['phase']} ({state['phase_time_left']})",
        True,
        TEXT_COLOR
    )
    screen.blit(phase_text, (40, 30))

    ped_text = font.render(
        f"PED queue: {state['p_queue']}",
        True,
        TEXT_COLOR
    )
    screen.blit(ped_text, (40, 90))

    # ----------------------------
    # Flip
    # ----------------------------
    pygame.display.flip()

pygame.quit()
