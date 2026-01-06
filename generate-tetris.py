#!/usr/bin/env python3
"""
Generate a retro pixel art arcade cabinet SVG with animated Tetris game inside.
8-bit aesthetic with scanlines, glow effects, and neon colors.
"""

import random
import copy

# Tetris game settings (inside the arcade screen)
GAME_COLS = 10
GAME_ROWS = 16
PIXEL_SIZE = 6

# Tetris pieces with rotations
PIECES = {
    'I': [[(0, 0), (0, 1), (0, 2), (0, 3)],
          [(0, 0), (1, 0), (2, 0), (3, 0)]],
    'O': [[(0, 0), (0, 1), (1, 0), (1, 1)]],
    'T': [[(0, 1), (1, 0), (1, 1), (1, 2)],
          [(0, 0), (1, 0), (1, 1), (2, 0)],
          [(0, 0), (0, 1), (0, 2), (1, 1)],
          [(0, 1), (1, 0), (1, 1), (2, 1)]],
    'S': [[(0, 1), (0, 2), (1, 0), (1, 1)],
          [(0, 0), (1, 0), (1, 1), (2, 1)]],
    'Z': [[(0, 0), (0, 1), (1, 1), (1, 2)],
          [(0, 1), (1, 0), (1, 1), (2, 0)]],
    'J': [[(0, 0), (1, 0), (1, 1), (1, 2)],
          [(0, 0), (0, 1), (1, 0), (2, 0)],
          [(0, 0), (0, 1), (0, 2), (1, 2)],
          [(0, 1), (1, 1), (2, 0), (2, 1)]],
    'L': [[(0, 2), (1, 0), (1, 1), (1, 2)],
          [(0, 0), (1, 0), (2, 0), (2, 1)],
          [(0, 0), (0, 1), (0, 2), (1, 0)],
          [(0, 0), (0, 1), (1, 1), (2, 1)]],
}

# Retro neon colors
PIECE_COLORS = {
    'I': '#00ffff',
    'O': '#ffff00',
    'T': '#ff00ff',
    'S': '#00ff00',
    'Z': '#ff0000',
    'J': '#0080ff',
    'L': '#ff8000',
}

EMPTY_COLOR = '#1a1a2e'
SCREEN_BG = '#0f0f1a'


class TetrisGame:
    def __init__(self):
        self.board = [[None for _ in range(GAME_COLS)] for _ in range(GAME_ROWS)]
        self.current_piece = None
        self.current_type = None
        self.current_rotation = 0
        self.current_row = 0
        self.current_col = 0
        self.frames = []
        self.lines_cleared = 0
        self.score = 0

    def spawn_piece(self):
        self.current_type = random.choice(list(PIECES.keys()))
        self.current_rotation = 0
        self.current_piece = PIECES[self.current_type][self.current_rotation]
        self.current_row = 0
        self.current_col = GAME_COLS // 2 - 2
        if not self.is_valid_position(self.current_row, self.current_col):
            return False
        return True

    def is_valid_position(self, row, col, piece=None):
        if piece is None:
            piece = self.current_piece
        for dr, dc in piece:
            r, c = row + dr, col + dc
            if r < 0 or r >= GAME_ROWS or c < 0 or c >= GAME_COLS:
                return False
            if r >= 0 and self.board[r][c] is not None:
                return False
        return True

    def try_rotate(self):
        if self.current_type == 'O':
            return False
        rotations = PIECES[self.current_type]
        new_rotation = (self.current_rotation + 1) % len(rotations)
        new_piece = rotations[new_rotation]
        for offset in [0, -1, 1, -2, 2]:
            if self.is_valid_position(self.current_row, self.current_col + offset, new_piece):
                self.current_rotation = new_rotation
                self.current_piece = new_piece
                self.current_col += offset
                return True
        return False

    def try_move(self, d_row, d_col):
        new_row = self.current_row + d_row
        new_col = self.current_col + d_col
        if self.is_valid_position(new_row, new_col):
            self.current_row = new_row
            self.current_col = new_col
            return True
        return False

    def lock_piece(self):
        for dr, dc in self.current_piece:
            r, c = self.current_row + dr, self.current_col + dc
            if 0 <= r < GAME_ROWS:
                self.board[r][c] = self.current_type

    def clear_lines(self):
        lines_to_clear = []
        for r in range(GAME_ROWS):
            if all(self.board[r][c] is not None for c in range(GAME_COLS)):
                lines_to_clear.append(r)
        for r in lines_to_clear:
            del self.board[r]
            self.board.insert(0, [None for _ in range(GAME_COLS)])
        if lines_to_clear:
            self.score += len(lines_to_clear) * 100
        return len(lines_to_clear)

    def capture_frame(self):
        frame = {
            'board': copy.deepcopy(self.board),
            'piece_type': self.current_type,
            'piece': copy.deepcopy(self.current_piece) if self.current_piece else None,
            'piece_row': self.current_row,
            'piece_col': self.current_col,
            'score': self.score,
        }
        self.frames.append(frame)

    def simulate_game(self, num_pieces=35):
        self.frames = []
        for _ in range(num_pieces):
            if not self.spawn_piece():
                self.board = [[None for _ in range(GAME_COLS)] for _ in range(GAME_ROWS)]
                self.score = 0
                self.spawn_piece()
            self.capture_frame()
            while True:
                action = random.random()
                if action < 0.2:
                    self.try_move(0, -1)
                elif action < 0.4:
                    self.try_move(0, 1)
                elif action < 0.5:
                    self.try_rotate()
                self.capture_frame()
                if not self.try_move(1, 0):
                    self.lock_piece()
                    cleared = self.clear_lines()
                    self.lines_cleared += cleared
                    self.current_piece = None
                    self.capture_frame()
                    break
        return self.frames


def create_arcade_svg(frames, frame_duration=0.12):
    """Create retro arcade cabinet SVG with animated Tetris."""

    # Cabinet dimensions
    cab_width = 200
    cab_height = 320

    # Screen area (inside cabinet)
    screen_x = 30
    screen_y = 40
    screen_width = GAME_COLS * PIXEL_SIZE + 20
    screen_height = GAME_ROWS * PIXEL_SIZE + 40

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
  <rect x="10" y="10" width="180" height="300" rx="8" fill="#2d1b4e"/>
  <rect x="15" y="15" width="170" height="290" rx="6" fill="#1a0f2e"/>

  <!-- Cabinet top decoration -->
  <rect x="20" y="12" width="160" height="20" rx="3" fill="#ff00ff" opacity="0.8"/>
  <text x="100" y="27" fill="#ffffff" font-family="monospace" font-size="12" text-anchor="middle" font-weight="bold" filter="url(#neon)">TETRIS</text>

  <!-- Screen bezel -->
  <rect x="{screen_x - 8}" y="{screen_y - 8}" width="{screen_width + 16}" height="{screen_height + 16}" rx="4" fill="#0a0a0a"/>
  <rect x="{screen_x - 4}" y="{screen_y - 4}" width="{screen_width + 8}" height="{screen_height + 8}" rx="2" fill="#1a1a1a"/>

  <!-- Screen background -->
  <rect x="{screen_x}" y="{screen_y}" width="{screen_width}" height="{screen_height}" fill="{SCREEN_BG}" rx="2"/>

  <!-- Game title on screen -->
  <text x="{screen_x + screen_width/2}" y="{screen_y + 12}" fill="#00ffff" font-family="monospace" font-size="8" text-anchor="middle" filter="url(#glow)">TETRIS</text>

  <!-- Score display -->
  <g id="score-display">
    <text x="{screen_x + screen_width - 5}" y="{screen_y + 12}" fill="#ffff00" font-family="monospace" font-size="6" text-anchor="end">
      <animate attributeName="opacity" values="1;0.7;1" dur="1s" repeatCount="indefinite"/>
      SCORE
    </text>
  </g>

  <!-- Game grid area -->
  <g transform="translate({screen_x + 10}, {screen_y + 20})" filter="url(#glow)">
'''

    # Create animated cells
    for row in range(GAME_ROWS):
        for col in range(GAME_COLS):
            x = col * PIXEL_SIZE
            y = row * PIXEL_SIZE

            colors = []
            for frame in frames:
                board = frame['board']
                piece = frame['piece']
                piece_row = frame['piece_row']
                piece_col = frame['piece_col']
                piece_type = frame['piece_type']

                cell_color = EMPTY_COLOR

                if board[row][col] is not None:
                    cell_color = PIECE_COLORS[board[row][col]]

                if piece is not None:
                    for dr, dc in piece:
                        pr, pc = piece_row + dr, piece_col + dc
                        if pr == row and pc == col:
                            cell_color = PIECE_COLORS[piece_type]
                            break

                colors.append(cell_color)

            if len(set(colors)) > 1:
                keyframe_values = ';'.join(colors)
                svg += f'''    <rect x="{x}" y="{y}" width="{PIXEL_SIZE-1}" height="{PIXEL_SIZE-1}" rx="1">
      <animate attributeName="fill" values="{keyframe_values}" dur="{total_duration}s" repeatCount="indefinite" calcMode="discrete"/>
    </rect>
'''
            else:
                svg += f'    <rect x="{x}" y="{y}" width="{PIXEL_SIZE-1}" height="{PIXEL_SIZE-1}" rx="1" fill="{colors[0]}"/>\n'

    svg += f'''  </g>

  <!-- Scanlines overlay -->
  <rect x="{screen_x}" y="{screen_y}" width="{screen_width}" height="{screen_height}" fill="url(#scanlines)" opacity="0.15"/>

  <!-- Screen reflection -->
  <ellipse cx="{screen_x + 20}" cy="{screen_y + 15}" rx="15" ry="8" fill="white" opacity="0.05"/>

  <!-- Control panel -->
  <rect x="25" y="195" width="150" height="60" rx="5" fill="#1a0f2e"/>
  <rect x="30" y="200" width="140" height="50" rx="3" fill="#2d1b4e"/>

  <!-- Joystick -->
  <circle cx="60" cy="225" r="15" fill="#0a0a0a"/>
  <circle cx="60" cy="225" r="12" fill="#1a1a1a"/>
  <circle cx="60" cy="223" r="8" fill="#ff0000">
    <animate attributeName="cy" values="223;225;223" dur="0.5s" repeatCount="indefinite"/>
  </circle>

  <!-- Buttons -->
  <circle cx="110" cy="220" r="10" fill="#ff00ff" filter="url(#glow)">
    <animate attributeName="opacity" values="1;0.6;1" dur="0.3s" repeatCount="indefinite"/>
  </circle>
  <circle cx="135" cy="225" r="10" fill="#00ffff" filter="url(#glow)">
    <animate attributeName="opacity" values="0.6;1;0.6" dur="0.3s" repeatCount="indefinite"/>
  </circle>
  <circle cx="155" cy="215" r="8" fill="#ffff00" filter="url(#glow)"/>

  <!-- Button labels -->
  <text x="110" y="223" fill="#000" font-family="monospace" font-size="6" text-anchor="middle">A</text>
  <text x="135" y="228" fill="#000" font-family="monospace" font-size="6" text-anchor="middle">B</text>

  <!-- Coin slot area -->
  <rect x="60" y="265" width="80" height="25" rx="3" fill="#0a0a0a"/>
  <rect x="85" y="270" width="30" height="4" rx="1" fill="#333"/>
  <text x="100" y="288" fill="#ffff00" font-family="monospace" font-size="6" text-anchor="middle">INSERT COIN</text>

  <!-- Cabinet legs -->
  <rect x="20" y="295" width="25" height="20" fill="#1a0f2e"/>
  <rect x="155" y="295" width="25" height="20" fill="#1a0f2e"/>

  <!-- Side art decorations -->
  <line x1="15" y1="100" x2="15" y2="250" stroke="#ff00ff" stroke-width="2" opacity="0.5"/>
  <line x1="185" y1="100" x2="185" y2="250" stroke="#00ffff" stroke-width="2" opacity="0.5"/>

  <!-- Animated marquee lights -->
  <g>
    <circle cx="25" cy="25" r="3" fill="#ff0000">
      <animate attributeName="opacity" values="1;0.3;1" dur="0.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="175" cy="25" r="3" fill="#ff0000">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="0.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="50" cy="25" r="3" fill="#ffff00">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="0.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="150" cy="25" r="3" fill="#ffff00">
      <animate attributeName="opacity" values="1;0.3;1" dur="0.5s" repeatCount="indefinite"/>
    </circle>
  </g>

</svg>'''

    return svg


if __name__ == '__main__':
    print("Simulating Tetris game...")
    game = TetrisGame()
    frames = game.simulate_game(num_pieces=30)
    print(f"Generated {len(frames)} frames, cleared {game.lines_cleared} lines")

    print("Creating arcade cabinet SVG...")
    svg_content = create_arcade_svg(frames, frame_duration=0.1)

    with open('tetris-contribution.svg', 'w') as f:
        f.write(svg_content)

    print("Generated tetris-contribution.svg")
