#!/usr/bin/env python3
"""
Generate a GitHub-style contribution graph SVG with animated WELCOME text.
Matches the exact size of GitHub's contribution graph with month/day labels.
"""

import math

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
TEXT_COLOR = '#ffffff'   # White text for labels

# Month labels (approximate positions for 53 weeks)
MONTHS = [
    (0, 'Jan'), (4, 'Feb'), (8, 'Mar'), (13, 'Apr'), (17, 'May'), (22, 'Jun'),
    (26, 'Jul'), (30, 'Aug'), (35, 'Sep'), (39, 'Oct'), (44, 'Nov'), (48, 'Dec')
]

# Day labels
DAYS = [(1, 'Mon'), (3, 'Wed'), (5, 'Fri')]

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


def generate_animation_frames(base_grid, num_frames=300):
    """Generate smooth frames with typing effect and color pulsing."""
    frames = []

    # Find all filled cells and sort by column then row for proper reveal
    filled_cells = []
    for col in range(GRID_COLS):
        for row in range(GRID_ROWS):
            if base_grid[row][col]:
                filled_cells.append((row, col))

    # Phase 1: Slower typing reveal (180 frames ~1.5 sec at 120fps)
    reveal_frames = 180

    for frame_idx in range(reveal_frames):
        # Calculate how many cells should be revealed by this frame
        progress = frame_idx / (reveal_frames - 1) if reveal_frames > 1 else 1
        cells_to_show = int(progress * len(filled_cells))

        revealed = set(filled_cells[:cells_to_show])

        frame = []
        for row in range(GRID_ROWS):
            frame_row = []
            for col in range(GRID_COLS):
                if (row, col) in revealed:
                    # Smooth color variation based on position
                    level = 2 + ((row + col + frame_idx) % 2)
                    frame_row.append(CONTRIB_COLORS[level])
                else:
                    frame_row.append(EMPTY_COLOR)
            frame.append(frame_row)
        frames.append(frame)

    # Phase 2: Smooth wave pulse (120 frames)
    pulse_frames = 120
    for frame_idx in range(pulse_frames):
        frame = []
        # Smooth wave using float math
        wave_offset = frame_idx * 0.15

        for row in range(GRID_ROWS):
            frame_row = []
            for col in range(GRID_COLS):
                if base_grid[row][col]:
                    # Smooth sine-like wave effect
                    wave = math.sin((col * 0.3) + wave_offset) * 0.5 + 0.5
                    if wave > 0.75:
                        level = 3
                    elif wave > 0.5:
                        level = 2
                    elif wave > 0.25:
                        level = 1
                    else:
                        level = 2
                    frame_row.append(CONTRIB_COLORS[level])
                else:
                    frame_row.append(EMPTY_COLOR)
            frame.append(frame_row)
        frames.append(frame)

    return frames


def create_contribution_svg(frames, fps=120):
    """Create a clean GitHub-style contribution graph SVG with labels."""

    # Layout offsets for labels
    left_margin = 40  # Space for day labels
    top_margin = 22   # Space for month labels
    bottom_margin = 25  # Space for legend

    # Calculate grid dimensions
    grid_width = GRID_COLS * (CELL_SIZE + CELL_GAP) - CELL_GAP
    grid_height = GRID_ROWS * (CELL_SIZE + CELL_GAP) - CELL_GAP

    # Total SVG dimensions
    width = grid_width + left_margin
    height = grid_height + top_margin + bottom_margin

    frame_duration = 1.0 / fps
    total_duration = len(frames) * frame_duration

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .month {{ fill: {TEXT_COLOR}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; }}
    .day {{ fill: {TEXT_COLOR}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; }}
    .legend {{ fill: {TEXT_COLOR}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; }}
  </style>

  <!-- Month labels -->
'''

    # Add month labels
    for col, month in MONTHS:
        x = left_margin + col * (CELL_SIZE + CELL_GAP)
        svg += f'  <text x="{x}" y="14" class="month">{month}</text>\n'

    svg += '\n  <!-- Day labels -->\n'

    # Add day labels
    for row, day in DAYS:
        y = top_margin + row * (CELL_SIZE + CELL_GAP) + 9  # +9 to vertically center
        svg += f'  <text x="0" y="{y}" class="day">{day}</text>\n'

    svg += '\n  <!-- Contribution grid -->\n'

    # Create cells
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = left_margin + col * (CELL_SIZE + CELL_GAP)
            y = top_margin + row * (CELL_SIZE + CELL_GAP)

            colors = [frame[row][col] for frame in frames]

            if len(set(colors)) > 1:
                keyframe_values = ';'.join(colors)
                svg += f'''  <rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" ry="2">
    <animate attributeName="fill" values="{keyframe_values}" dur="{total_duration:.3f}s" repeatCount="indefinite" calcMode="discrete"/>
  </rect>
'''
            else:
                svg += f'  <rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" ry="2" fill="{colors[0]}"/>\n'

    # Add legend (Less ... More)
    legend_y = top_margin + grid_height + 15
    legend_x = left_margin + grid_width - 130  # Position from right

    svg += f'''
  <!-- Legend -->
  <text x="{legend_x}" y="{legend_y + 8}" class="legend">Less</text>
  <rect x="{legend_x + 30}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" ry="2" fill="{EMPTY_COLOR}"/>
  <rect x="{legend_x + 43}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" ry="2" fill="{CONTRIB_COLORS[0]}"/>
  <rect x="{legend_x + 56}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" ry="2" fill="{CONTRIB_COLORS[1]}"/>
  <rect x="{legend_x + 69}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" ry="2" fill="{CONTRIB_COLORS[2]}"/>
  <rect x="{legend_x + 82}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" ry="2" fill="{CONTRIB_COLORS[3]}"/>
  <text x="{legend_x + 97}" y="{legend_y + 8}" class="legend">More</text>
'''

    svg += '</svg>'

    return svg


if __name__ == '__main__':
    print("Building WELCOME contribution grid...")
    base_grid = build_welcome_grid()

    print("Generating animation frames at 120fps...")
    frames = generate_animation_frames(base_grid, num_frames=300)
    print(f"Generated {len(frames)} frames")

    print("Creating contribution graph SVG...")
    svg_content = create_contribution_svg(frames, fps=120)

    with open('welcome-contribution.svg', 'w') as f:
        f.write(svg_content)

    print("Generated welcome-contribution.svg")
