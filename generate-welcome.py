#!/usr/bin/env python3
"""
Generate a GitHub-style contribution graph SVG with animated WELCOME text.
Matches the exact size of GitHub's contribution graph.
"""

import random

# GitHub contribution graph dimensions (actual GitHub sizes)
GRID_COLS = 53   # 53 weeks in a year
GRID_ROWS = 7    # 7 days per week
CELL_SIZE = 10   # GitHub uses 10px cells
CELL_GAP = 3     # 3px gap between cells

# GitHub contribution green colors (dark mode)
CONTRIB_COLORS = [
    '#0e4429',  # Level 1
    '#006d32',  # Level 2
    '#26a641',  # Level 3
    '#39d353',  # Level 4
]
EMPTY_COLOR = '#161b22'  # GitHub dark mode empty cell

# Letter patterns (7 rows tall to match contribution graph)
LETTERS = {
    'W': [
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,1,0,1],
        [1,1,0,1,1],
        [1,0,0,0,1],
    ],
    'E': [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
    ],
    'L': [
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
    ],
    'C': [
        [0,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [0,1,1,1,1],
    ],
    'O': [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0],
    ],
    'M': [
        [1,0,0,0,1],
        [1,1,0,1,1],
        [1,0,1,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
    ],
}


def build_welcome_grid():
    """Build the full grid with WELCOME spelled out."""
    word = "WELCOME"
    grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    letter_width = 5
    spacing = 2
    total_width = len(word) * letter_width + (len(word) - 1) * spacing
    start_col = (GRID_COLS - total_width) // 2

    col = start_col
    for char in word:
        if char in LETTERS:
            letter = LETTERS[char]
            for row in range(GRID_ROWS):
                for c in range(letter_width):
                    if col + c < GRID_COLS:
                        grid[row][col + c] = letter[row][c]
            col += letter_width + spacing

    return grid


def generate_animation_frames(base_grid, num_frames=60):
    """Generate frames with typing effect and color pulsing."""
    frames = []

    filled_cells = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if base_grid[row][col]:
                filled_cells.append((row, col))

    filled_cells.sort(key=lambda x: (x[1], x[0]))

    # Phase 1: Typing reveal
    reveal_frames = 30
    cells_per_frame = max(1, len(filled_cells) // reveal_frames)

    revealed = set()
    for frame_idx in range(reveal_frames):
        cells_to_reveal = min(cells_per_frame, len(filled_cells) - len(revealed))
        for _ in range(cells_to_reveal):
            if len(revealed) < len(filled_cells):
                revealed.add(filled_cells[len(revealed)])

        frame = []
        for row in range(GRID_ROWS):
            frame_row = []
            for col in range(GRID_COLS):
                if (row, col) in revealed:
                    level = random.randint(2, 3)
                    frame_row.append(CONTRIB_COLORS[level])
                else:
                    frame_row.append(EMPTY_COLOR)
            frame.append(frame_row)
        frames.append(frame)

    # Phase 2: Wave pulse
    pulse_frames = 30
    for frame_idx in range(pulse_frames):
        frame = []
        wave_offset = frame_idx / 5.0

        for row in range(GRID_ROWS):
            frame_row = []
            for col in range(GRID_COLS):
                if base_grid[row][col]:
                    wave = (col + wave_offset) % 4
                    if wave < 1:
                        level = 3
                    elif wave < 2:
                        level = 2
                    elif wave < 3:
                        level = 1
                    else:
                        level = 2
                    frame_row.append(CONTRIB_COLORS[level])
                else:
                    frame_row.append(EMPTY_COLOR)
            frame.append(frame_row)
        frames.append(frame)

    return frames


def create_contribution_svg(frames, frame_duration=0.12):
    """Create a clean GitHub-style contribution graph SVG."""

    # Calculate dimensions (matches GitHub's actual graph)
    width = GRID_COLS * (CELL_SIZE + CELL_GAP) - CELL_GAP
    height = GRID_ROWS * (CELL_SIZE + CELL_GAP) - CELL_GAP

    total_duration = len(frames) * frame_duration

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
'''

    # Create cells
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (CELL_SIZE + CELL_GAP)
            y = row * (CELL_SIZE + CELL_GAP)

            colors = [frame[row][col] for frame in frames]

            if len(set(colors)) > 1:
                keyframe_values = ';'.join(colors)
                svg += f'''  <rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" ry="2">
    <animate attributeName="fill" values="{keyframe_values}" dur="{total_duration}s" repeatCount="indefinite" calcMode="discrete"/>
  </rect>
'''
            else:
                svg += f'  <rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" ry="2" fill="{colors[0]}"/>\n'

    svg += '</svg>'

    return svg


if __name__ == '__main__':
    print("Building WELCOME contribution grid...")
    base_grid = build_welcome_grid()

    print("Generating animation frames...")
    frames = generate_animation_frames(base_grid, num_frames=60)
    print(f"Generated {len(frames)} frames")

    print("Creating contribution graph SVG...")
    svg_content = create_contribution_svg(frames, frame_duration=0.12)

    with open('welcome-contribution.svg', 'w') as f:
        f.write(svg_content)

    print("Generated welcome-contribution.svg")
