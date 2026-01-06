#!/usr/bin/env python3
"""
Generate an animated SVG of a real Tetris game simulation with proper rules:
- Pieces fall and stack
- Collision detection
- Line clearing
- Game restarts when board fills up
"""

import random
import copy

# Board dimensions (wider for better gameplay, height for Tetris)
COLS = 10
ROWS = 20
CELL_SIZE = 12
CELL_GAP = 2
TOTAL_CELL = CELL_SIZE + CELL_GAP

# Tetris piece definitions (row, col offsets from origin)
# Standard Tetris rotation system
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

PIECE_COLORS = {
    'I': '#00f0f0',
    'O': '#f0f000',
    'T': '#a000f0',
    'S': '#00f000',
    'Z': '#f00000',
    'J': '#0000f0',
    'L': '#f0a000',
}

EMPTY_COLOR = '#161b22'
GRID_COLOR = '#21262d'


class TetrisGame:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_piece = None
        self.current_type = None
        self.current_rotation = 0
        self.current_row = 0
        self.current_col = 0
        self.frames = []
        self.lines_cleared = 0

    def spawn_piece(self):
        """Spawn a new piece at the top."""
        self.current_type = random.choice(list(PIECES.keys()))
        self.current_rotation = 0
        self.current_piece = PIECES[self.current_type][self.current_rotation]
        self.current_row = 0
        self.current_col = COLS // 2 - 2

        # Check if spawn position is valid (game over condition)
        if not self.is_valid_position(self.current_row, self.current_col):
            return False
        return True

    def is_valid_position(self, row, col, piece=None):
        """Check if piece position is valid."""
        if piece is None:
            piece = self.current_piece
        for dr, dc in piece:
            r, c = row + dr, col + dc
            if r < 0 or r >= ROWS or c < 0 or c >= COLS:
                return False
            if r >= 0 and self.board[r][c] is not None:
                return False
        return True

    def try_rotate(self):
        """Try to rotate the current piece."""
        if self.current_type == 'O':
            return False

        rotations = PIECES[self.current_type]
        new_rotation = (self.current_rotation + 1) % len(rotations)
        new_piece = rotations[new_rotation]

        # Try rotation, with wall kicks
        for offset in [0, -1, 1, -2, 2]:
            if self.is_valid_position(self.current_row, self.current_col + offset, new_piece):
                self.current_rotation = new_rotation
                self.current_piece = new_piece
                self.current_col += offset
                return True
        return False

    def try_move(self, d_row, d_col):
        """Try to move the piece."""
        new_row = self.current_row + d_row
        new_col = self.current_col + d_col
        if self.is_valid_position(new_row, new_col):
            self.current_row = new_row
            self.current_col = new_col
            return True
        return False

    def lock_piece(self):
        """Lock the current piece into the board."""
        for dr, dc in self.current_piece:
            r, c = self.current_row + dr, self.current_col + dc
            if 0 <= r < ROWS:
                self.board[r][c] = self.current_type

    def clear_lines(self):
        """Clear completed lines and return count."""
        lines_to_clear = []
        for r in range(ROWS):
            if all(self.board[r][c] is not None for c in range(COLS)):
                lines_to_clear.append(r)

        for r in lines_to_clear:
            del self.board[r]
            self.board.insert(0, [None for _ in range(COLS)])

        return len(lines_to_clear)

    def capture_frame(self):
        """Capture current game state as a frame."""
        frame = {
            'board': copy.deepcopy(self.board),
            'piece_type': self.current_type,
            'piece': copy.deepcopy(self.current_piece) if self.current_piece else None,
            'piece_row': self.current_row,
            'piece_col': self.current_col,
        }
        self.frames.append(frame)

    def simulate_game(self, num_pieces=50):
        """Simulate a full game."""
        self.frames = []

        for _ in range(num_pieces):
            if not self.spawn_piece():
                # Game over - reset board
                self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
                self.spawn_piece()

            self.capture_frame()

            # Simulate piece falling with occasional moves/rotations
            while True:
                # Random actions for variety
                action = random.random()
                if action < 0.15:
                    self.try_move(0, -1)  # Move left
                elif action < 0.30:
                    self.try_move(0, 1)   # Move right
                elif action < 0.40:
                    self.try_rotate()

                self.capture_frame()

                # Try to move down
                if not self.try_move(1, 0):
                    # Can't move down, lock piece
                    self.lock_piece()
                    cleared = self.clear_lines()
                    self.lines_cleared += cleared

                    # Capture frame after locking (and line clear)
                    self.current_piece = None
                    self.capture_frame()
                    break

        return self.frames


def create_svg(frames, frame_duration=0.08):
    """Create animated SVG from game frames."""
    width = COLS * TOTAL_CELL + 20
    height = ROWS * TOTAL_CELL + 40
    total_duration = len(frames) * frame_duration

    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')

    # Styles
    svg_parts.append('<style>')
    svg_parts.append('  .cell { rx: 2; ry: 2; }')
    svg_parts.append('  text { font-family: monospace; }')
    svg_parts.append('</style>')

    # Background
    svg_parts.append(f'<rect width="{width}" height="{height}" fill="#0d1117"/>')

    # Title
    svg_parts.append(f'<text x="{width/2}" y="15" fill="#58a6ff" font-size="11" text-anchor="middle" font-weight="bold">TETRIS</text>')

    # Grid background
    svg_parts.append('<g transform="translate(10, 25)">')
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TOTAL_CELL
            y = row * TOTAL_CELL
            svg_parts.append(f'<rect class="cell" x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{GRID_COLOR}" opacity="0.3"/>')
    svg_parts.append('</g>')

    # Animated cells - use CSS keyframes for each cell position
    svg_parts.append('<g transform="translate(10, 25)">')

    # For each cell position, create keyframes based on what's there each frame
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TOTAL_CELL
            y = row * TOTAL_CELL

            # Build keyframe values for this cell
            colors = []
            for frame in frames:
                board = frame['board']
                piece = frame['piece']
                piece_row = frame['piece_row']
                piece_col = frame['piece_col']
                piece_type = frame['piece_type']

                # Check if current piece occupies this cell
                cell_color = EMPTY_COLOR

                # First check board
                if board[row][col] is not None:
                    cell_color = PIECE_COLORS[board[row][col]]

                # Then check active piece
                if piece is not None:
                    for dr, dc in piece:
                        pr, pc = piece_row + dr, piece_col + dc
                        if pr == row and pc == col:
                            cell_color = PIECE_COLORS[piece_type]
                            break

                colors.append(cell_color)

            # Only create animated rect if colors change
            if len(set(colors)) > 1:
                # Create keyframes string
                keyframe_values = ';'.join(colors)
                svg_parts.append(f'<rect class="cell" x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}">')
                svg_parts.append(f'  <animate attributeName="fill" values="{keyframe_values}" dur="{total_duration}s" repeatCount="indefinite" calcMode="discrete"/>')
                svg_parts.append('</rect>')
            else:
                # Static cell
                svg_parts.append(f'<rect class="cell" x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{colors[0]}"/>')

    svg_parts.append('</g>')
    svg_parts.append('</svg>')

    return '\n'.join(svg_parts)


if __name__ == '__main__':
    print("Simulating Tetris game...")
    game = TetrisGame()
    frames = game.simulate_game(num_pieces=40)
    print(f"Generated {len(frames)} frames, cleared {game.lines_cleared} lines")

    print("Creating SVG animation...")
    svg_content = create_svg(frames, frame_duration=0.1)

    with open('tetris-contribution.svg', 'w') as f:
        f.write(svg_content)

    print("Generated tetris-contribution.svg")
