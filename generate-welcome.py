#!/usr/bin/env python3
"""
Generate a retro pixel art arcade cabinet SVG with animated WELCOME contribution graph.
8-bit aesthetic with scanlines, glow effects, and GitHub green colors.
"""

import random

# Contribution grid settings (mimics GitHub contribution graph)
GRID_COLS = 42  # Enough for WELCOME with spacing
GRID_ROWS = 7   # GitHub uses 7 rows (days of week)
PIXEL_SIZE = 5

# GitHub contribution green colors (light to dark)
CONTRIB_COLORS = [
    '#0e4429',  # Level 1 - darkest green
    '#006d32',  # Level 2
    '#26a641',  # Level 3
    '#39d353',  # Level 4 - brightest green
]
EMPTY_COLOR = '#161b22'  # GitHub dark mode empty cell
SCREEN_BG = '#0d1117'    # GitHub dark mode background

# Letter patterns (7 rows tall to match contribution graph weeks)
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

    # Calculate starting position to center the word
    letter_width = 5
    spacing = 1
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

    # Find all filled cells
    filled_cells = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if base_grid[row][col]:
                filled_cells.append((row, col))

    # Sort by column (left to right reveal)
    filled_cells.sort(key=lambda x: (x[1], x[0]))

    # Phase 1: Reveal letters one by one (typing effect)
    reveal_frames = 30
    cells_per_frame = max(1, len(filled_cells) // reveal_frames)

    revealed = set()
    for frame_idx in range(reveal_frames):
        # Reveal more cells
        cells_to_reveal = min(cells_per_frame, len(filled_cells) - len(revealed))
        for _ in range(cells_to_reveal):
            if len(revealed) < len(filled_cells):
                revealed.add(filled_cells[len(revealed)])

        # Build frame
        frame = []
        for row in range(GRID_ROWS):
            frame_row = []
            for col in range(GRID_COLS):
                if (row, col) in revealed:
                    # Vary the green intensity for visual interest
                    level = random.randint(2, 3)
                    frame_row.append(CONTRIB_COLORS[level])
                else:
                    frame_row.append(EMPTY_COLOR)
            frame.append(frame_row)
        frames.append(frame)

    # Phase 2: Pulse animation (all letters visible, colors shifting)
    pulse_frames = 30
    for frame_idx in range(pulse_frames):
        frame = []
        # Create wave effect
        wave_offset = frame_idx / 5.0

        for row in range(GRID_ROWS):
            frame_row = []
            for col in range(GRID_COLS):
                if base_grid[row][col]:
                    # Create pulsing wave effect
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


def create_arcade_svg(frames, frame_duration=0.15):
    """Create retro arcade cabinet SVG with animated contribution graph."""

    # Cabinet dimensions
    cab_width = 280
    cab_height = 200

    # Screen area (inside cabinet)
    screen_x = 25
    screen_y = 35
    screen_width = GRID_COLS * PIXEL_SIZE + 20
    screen_height = GRID_ROWS * PIXEL_SIZE + 40

    total_duration = len(frames) * frame_duration

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{cab_width}" height="{cab_height}" viewBox="0 0 {cab_width} {cab_height}">
  <defs>
    <!-- Scanline pattern -->
    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="2" fill="rgba(0,0,0,0.3)"/>
    </pattern>

    <!-- Screen glow -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Neon glow for text -->
    <filter id="neon" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Cabinet body -->
  <rect x="5" y="5" width="{cab_width - 10}" height="{cab_height - 10}" rx="8" fill="#2d1b4e"/>
  <rect x="10" y="10" width="{cab_width - 20}" height="{cab_height - 20}" rx="6" fill="#1a0f2e"/>

  <!-- Cabinet top decoration -->
  <rect x="15" y="8" width="{cab_width - 30}" height="18" rx="3" fill="#39d353" opacity="0.8"/>
  <text x="{cab_width/2}" y="21" fill="#ffffff" font-family="monospace" font-size="10" text-anchor="middle" font-weight="bold" filter="url(#neon)">CONTRIBUTION GRAPH</text>

  <!-- Screen bezel -->
  <rect x="{screen_x - 6}" y="{screen_y - 6}" width="{screen_width + 12}" height="{screen_height + 12}" rx="4" fill="#0a0a0a"/>
  <rect x="{screen_x - 3}" y="{screen_y - 3}" width="{screen_width + 6}" height="{screen_height + 6}" rx="2" fill="#161b22"/>

  <!-- Screen background -->
  <rect x="{screen_x}" y="{screen_y}" width="{screen_width}" height="{screen_height}" fill="{SCREEN_BG}" rx="2"/>

  <!-- GitHub-style header -->
  <text x="{screen_x + 10}" y="{screen_y + 12}" fill="#8b949e" font-family="monospace" font-size="7">contributions in the last year</text>

  <!-- Contribution grid area -->
  <g transform="translate({screen_x + 10}, {screen_y + 20})" filter="url(#glow)">
'''

    # Create animated cells
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * PIXEL_SIZE
            y = row * PIXEL_SIZE

            colors = [frame[row][col] for frame in frames]

            if len(set(colors)) > 1:
                keyframe_values = ';'.join(colors)
                svg += f'''    <rect x="{x}" y="{y}" width="{PIXEL_SIZE-1}" height="{PIXEL_SIZE-1}" rx="1">
      <animate attributeName="fill" values="{keyframe_values}" dur="{total_duration}s" repeatCount="indefinite" calcMode="discrete"/>
    </rect>
'''
            else:
                svg += f'    <rect x="{x}" y="{y}" width="{PIXEL_SIZE-1}" height="{PIXEL_SIZE-1}" rx="1" fill="{colors[0]}"/>\n'

    svg += f'''  </g>

  <!-- Legend -->
  <g transform="translate({screen_x + screen_width - 80}, {screen_y + screen_height - 15})">
    <text x="0" y="8" fill="#8b949e" font-family="monospace" font-size="6">Less</text>
    <rect x="22" y="2" width="8" height="8" rx="1" fill="{EMPTY_COLOR}"/>
    <rect x="32" y="2" width="8" height="8" rx="1" fill="{CONTRIB_COLORS[0]}"/>
    <rect x="42" y="2" width="8" height="8" rx="1" fill="{CONTRIB_COLORS[1]}"/>
    <rect x="52" y="2" width="8" height="8" rx="1" fill="{CONTRIB_COLORS[2]}"/>
    <rect x="62" y="2" width="8" height="8" rx="1" fill="{CONTRIB_COLORS[3]}"/>
    <text x="75" y="8" fill="#8b949e" font-family="monospace" font-size="6">More</text>
  </g>

  <!-- Scanlines overlay -->
  <rect x="{screen_x}" y="{screen_y}" width="{screen_width}" height="{screen_height}" fill="url(#scanlines)" opacity="0.1"/>

  <!-- Screen reflection -->
  <ellipse cx="{screen_x + 30}" cy="{screen_y + 15}" rx="20" ry="8" fill="white" opacity="0.03"/>

  <!-- Side art decorations -->
  <line x1="10" y1="60" x2="10" y2="140" stroke="#39d353" stroke-width="2" opacity="0.5"/>
  <line x1="{cab_width - 10}" y1="60" x2="{cab_width - 10}" y2="140" stroke="#39d353" stroke-width="2" opacity="0.5"/>

  <!-- Bottom decoration -->
  <rect x="20" y="{cab_height - 25}" width="{cab_width - 40}" height="12" rx="3" fill="#161b22"/>
  <text x="{cab_width/2}" y="{cab_height - 16}" fill="#39d353" font-family="monospace" font-size="8" text-anchor="middle" filter="url(#glow)">
    <animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/>
    github.com
  </text>

  <!-- Animated corner lights -->
  <g>
    <circle cx="18" cy="18" r="3" fill="#39d353">
      <animate attributeName="opacity" values="1;0.3;1" dur="0.8s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{cab_width - 18}" cy="18" r="3" fill="#39d353">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="0.8s" repeatCount="indefinite"/>
    </circle>
  </g>

</svg>'''

    return svg


if __name__ == '__main__':
    print("Building WELCOME contribution grid...")
    base_grid = build_welcome_grid()

    print("Generating animation frames...")
    frames = generate_animation_frames(base_grid, num_frames=60)
    print(f"Generated {len(frames)} frames")

    print("Creating arcade cabinet SVG...")
    svg_content = create_arcade_svg(frames, frame_duration=0.12)

    with open('welcome-contribution.svg', 'w') as f:
        f.write(svg_content)

    print("Generated welcome-contribution.svg")
