#!/usr/bin/env python3
"""
Generate an animated SVG of Tetris playing on a GitHub contribution graph style grid.
"""

import random
import math

# Contribution graph dimensions (52 weeks x 7 days)
COLS = 52
ROWS = 7
CELL_SIZE = 11
CELL_GAP = 3
TOTAL_CELL = CELL_SIZE + CELL_GAP

# Colors matching GitHub's contribution colors
COLORS = {
    'empty': '#161b22',
    'level1': '#0e4429',
    'level2': '#006d32',
    'level3': '#26a641',
    'level4': '#39d353',
}

# Tetris piece definitions (each piece as list of relative positions)
PIECES = {
    'I': [(0, 0), (0, 1), (0, 2), (0, 3)],
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'T': [(0, 0), (0, 1), (0, 2), (1, 1)],
    'S': [(0, 1), (0, 2), (1, 0), (1, 1)],
    'Z': [(0, 0), (0, 1), (1, 1), (1, 2)],
    'J': [(0, 0), (1, 0), (1, 1), (1, 2)],
    'L': [(0, 2), (1, 0), (1, 1), (1, 2)],
}

PIECE_COLORS = {
    'I': '#00f0f0',
    'O': '#f0f000',
    'T': '#a000f0',
    'S': '#00f000',
    'Z': '#f00000',
    'J': '#0000f0',
    'L': '#f0a000',
}


def generate_base_grid():
    """Generate a random contribution-style base grid."""
    grid = []
    for row in range(ROWS):
        grid_row = []
        for col in range(COLS):
            # Random contribution levels with higher chance of empty
            r = random.random()
            if r < 0.4:
                grid_row.append('empty')
            elif r < 0.6:
                grid_row.append('level1')
            elif r < 0.75:
                grid_row.append('level2')
            elif r < 0.9:
                grid_row.append('level3')
            else:
                grid_row.append('level4')
        grid.append(grid_row)
    return grid


def generate_tetris_animation():
    """Generate falling tetris pieces animation frames."""
    frames = []
    num_pieces = 8
    frame_duration = 0.15

    for piece_idx in range(num_pieces):
        piece_type = random.choice(list(PIECES.keys()))
        piece_shape = PIECES[piece_type]
        piece_color = PIECE_COLORS[piece_type]

        # Random starting column
        start_col = random.randint(5, COLS - 10)

        # Generate frames for this piece falling
        for y_offset in range(-4, ROWS + 1):
            frame = {
                'piece_type': piece_type,
                'piece_shape': piece_shape,
                'piece_color': piece_color,
                'col': start_col,
                'row': y_offset,
                'duration': frame_duration,
            }
            frames.append(frame)

    return frames


def create_svg():
    """Create the complete animated SVG."""
    width = COLS * TOTAL_CELL + 20
    height = ROWS * TOTAL_CELL + 20

    base_grid = generate_base_grid()
    frames = generate_tetris_animation()

    # Calculate total animation duration
    total_duration = len(frames) * 0.15

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>',
        '  .cell { rx: 2; ry: 2; }',
        '  @keyframes tetris-fall {',
    ]

    # Generate keyframes for each falling piece animation
    current_time = 0
    keyframe_percents = []

    for i, frame in enumerate(frames):
        percent = (i / len(frames)) * 100
        keyframe_percents.append((percent, frame))

    svg_parts.append('  }')
    svg_parts.append('</style>')

    # Background
    svg_parts.append(f'<rect width="{width}" height="{height}" fill="#0d1117"/>')

    # Draw base contribution grid
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TOTAL_CELL + 10
            y = row * TOTAL_CELL + 10
            color = COLORS[base_grid[row][col]]
            svg_parts.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{color}"/>'
            )

    # Create animated tetris pieces using CSS animations
    piece_animations = []
    time_offset = 0

    for piece_idx in range(8):
        piece_type = random.choice(list(PIECES.keys()))
        piece_shape = PIECES[piece_type]
        piece_color = PIECE_COLORS[piece_type]
        start_col = random.randint(5, COLS - 10)

        piece_id = f'piece-{piece_idx}'
        fall_duration = 1.5

        # Create piece group with animation
        svg_parts.append(f'<g id="{piece_id}">')
        svg_parts.append(f'  <animateTransform attributeName="transform" type="translate"')
        svg_parts.append(f'    values="0,-{(ROWS + 4) * TOTAL_CELL};0,{ROWS * TOTAL_CELL}"')
        svg_parts.append(f'    dur="{fall_duration}s" begin="{time_offset}s"')
        svg_parts.append(f'    repeatCount="indefinite" calcMode="linear"/>')

        # Draw piece blocks
        for (dr, dc) in piece_shape:
            x = (start_col + dc) * TOTAL_CELL + 10
            y = dr * TOTAL_CELL + 10
            svg_parts.append(
                f'  <rect class="cell" x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{piece_color}" opacity="0.9"/>'
            )

        svg_parts.append('</g>')
        time_offset += fall_duration / 2  # Overlap pieces

    svg_parts.append('</svg>')

    return '\n'.join(svg_parts)


def create_advanced_svg():
    """Create a more polished animated SVG with smooth tetris gameplay."""
    width = COLS * TOTAL_CELL + 20
    height = ROWS * TOTAL_CELL + 40

    base_grid = generate_base_grid()

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="1" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="{width}" height="{height}" fill="#0d1117"/>

  <!-- Title -->
  <text x="{width/2}" y="15" fill="#58a6ff" font-family="monospace" font-size="10" text-anchor="middle">TETRIS x CONTRIBUTIONS</text>

  <!-- Contribution Grid -->
  <g transform="translate(0, 25)">
'''

    # Draw base grid
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TOTAL_CELL + 10
            y = row * TOTAL_CELL
            color = COLORS[base_grid[row][col]]
            svg += f'    <rect class="cell" x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{color}" rx="2"/>\n'

    # Add animated falling pieces
    pieces_svg = ""
    time_offset = 0

    for i in range(6):
        piece_type = list(PIECES.keys())[i % len(PIECES)]
        piece_shape = PIECES[piece_type]
        piece_color = PIECE_COLORS[piece_type]
        start_col = 5 + (i * 7) % (COLS - 10)

        fall_duration = 2.0 + random.random() * 0.5
        start_y = -4 * TOTAL_CELL
        end_y = ROWS * TOTAL_CELL

        pieces_svg += f'''
    <!-- Piece {i+1}: {piece_type} -->
    <g filter="url(#glow)">
      <animateTransform attributeName="transform" type="translate"
        values="0,{start_y};0,{end_y}"
        dur="{fall_duration}s" begin="{time_offset}s"
        repeatCount="indefinite"/>
'''
        for (dr, dc) in piece_shape:
            x = (start_col + dc) * TOTAL_CELL + 10
            y = dr * TOTAL_CELL
            pieces_svg += f'      <rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{piece_color}" rx="2" opacity="0.85"/>\n'

        pieces_svg += '    </g>\n'
        time_offset += fall_duration * 0.4

    svg += pieces_svg
    svg += '''  </g>
</svg>'''

    return svg


if __name__ == '__main__':
    svg_content = create_advanced_svg()

    with open('tetris-contribution.svg', 'w') as f:
        f.write(svg_content)

    print("Generated tetris-contribution.svg")
