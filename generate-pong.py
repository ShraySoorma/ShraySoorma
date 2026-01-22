#!/usr/bin/env python3
"""
Generate a GitHub-style contribution graph SVG with animated Pong game.
Matches the exact size of GitHub's contribution graph with month/day labels.
"""

# GitHub contribution graph dimensions (actual GitHub sizes)
GRID_COLS = 53   # 53 weeks in a year
GRID_ROWS = 7    # 7 days per week
CELL_SIZE = 10   # GitHub uses 10px cells
CELL_GAP = 3     # 3px gap between cells

# GitHub contribution green colors (dark mode)
CONTRIB_COLORS = [
    '#0e4429',  # Level 1 - dim
    '#006d32',  # Level 2
    '#26a641',  # Level 3 - medium (paddles)
    '#39d353',  # Level 4 - bright (ball)
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

# Pong game constants
PADDLE_HEIGHT = 3
LEFT_PADDLE_COL = 1
RIGHT_PADDLE_COL = 51
CENTER_COL = 26


class PongGame:
    """Simulates a Pong game on the contribution grid."""

    def __init__(self):
        # Ball position and velocity
        self.ball_x = GRID_COLS // 2
        self.ball_y = GRID_ROWS // 2
        self.ball_vx = 1
        self.ball_vy = 1

        # Paddle positions (top of paddle)
        self.left_paddle_y = (GRID_ROWS - PADDLE_HEIGHT) // 2
        self.right_paddle_y = (GRID_ROWS - PADDLE_HEIGHT) // 2

    def _clamp_paddle(self, y):
        """Keep paddle within grid bounds."""
        return max(0, min(GRID_ROWS - PADDLE_HEIGHT, y))

    def _paddle_cells(self, col, paddle_y):
        """Return set of cells occupied by a paddle."""
        return {(row, col) for row in range(paddle_y, paddle_y + PADDLE_HEIGHT)}

    def update(self):
        """Update game state for one frame."""
        # Move paddles toward ball with slight delay for realism
        # Left paddle tracks ball when ball is on left side
        if self.ball_x < GRID_COLS // 2:
            target_y = self.ball_y - PADDLE_HEIGHT // 2
            if self.left_paddle_y < target_y:
                self.left_paddle_y += 1
            elif self.left_paddle_y > target_y:
                self.left_paddle_y -= 1

        # Right paddle tracks ball when ball is on right side
        if self.ball_x >= GRID_COLS // 2:
            target_y = self.ball_y - PADDLE_HEIGHT // 2
            if self.right_paddle_y < target_y:
                self.right_paddle_y += 1
            elif self.right_paddle_y > target_y:
                self.right_paddle_y -= 1

        # Clamp paddles
        self.left_paddle_y = self._clamp_paddle(self.left_paddle_y)
        self.right_paddle_y = self._clamp_paddle(self.right_paddle_y)

        # Calculate next ball position
        next_x = self.ball_x + self.ball_vx
        next_y = self.ball_y + self.ball_vy

        # Bounce off top and bottom walls
        if next_y < 0:
            next_y = 0
            self.ball_vy = -self.ball_vy
        elif next_y >= GRID_ROWS:
            next_y = GRID_ROWS - 1
            self.ball_vy = -self.ball_vy

        # Check left paddle collision
        if next_x <= LEFT_PADDLE_COL + 1 and self.ball_vx < 0:
            paddle_cells = self._paddle_cells(LEFT_PADDLE_COL, self.left_paddle_y)
            # Check if ball would hit paddle
            for py in range(self.left_paddle_y, self.left_paddle_y + PADDLE_HEIGHT):
                if next_y == py:
                    next_x = LEFT_PADDLE_COL + 2
                    self.ball_vx = -self.ball_vx
                    break
            else:
                # Ball missed paddle - wrap around for continuous play
                if next_x < 0:
                    next_x = GRID_COLS - 1

        # Check right paddle collision
        if next_x >= RIGHT_PADDLE_COL - 1 and self.ball_vx > 0:
            paddle_cells = self._paddle_cells(RIGHT_PADDLE_COL, self.right_paddle_y)
            # Check if ball would hit paddle
            for py in range(self.right_paddle_y, self.right_paddle_y + PADDLE_HEIGHT):
                if next_y == py:
                    next_x = RIGHT_PADDLE_COL - 2
                    self.ball_vx = -self.ball_vx
                    break
            else:
                # Ball missed paddle - wrap around for continuous play
                if next_x >= GRID_COLS:
                    next_x = 0

        self.ball_x = next_x
        self.ball_y = next_y

    def get_frame(self):
        """Return current grid state as 2D array of colors."""
        grid = [[EMPTY_COLOR for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

        # Draw center line (dashed, every other cell)
        for row in range(GRID_ROWS):
            if row % 2 == 0:
                grid[row][CENTER_COL] = CONTRIB_COLORS[0]  # Dim green

        # Draw left paddle
        for row in range(self.left_paddle_y, self.left_paddle_y + PADDLE_HEIGHT):
            if 0 <= row < GRID_ROWS:
                grid[row][LEFT_PADDLE_COL] = CONTRIB_COLORS[2]  # Medium green

        # Draw right paddle
        for row in range(self.right_paddle_y, self.right_paddle_y + PADDLE_HEIGHT):
            if 0 <= row < GRID_ROWS:
                grid[row][RIGHT_PADDLE_COL] = CONTRIB_COLORS[2]  # Medium green

        # Draw ball
        if 0 <= self.ball_y < GRID_ROWS and 0 <= self.ball_x < GRID_COLS:
            grid[self.ball_y][self.ball_x] = CONTRIB_COLORS[3]  # Brightest green

        return grid


def simulate_pong_game(num_game_updates=480, frames_per_update=2):
    """Run Pong game simulation and capture each frame.

    Args:
        num_game_updates: Number of game state updates
        frames_per_update: Render frames per game update (higher = slower game)
    """
    game = PongGame()
    frames = []

    for _ in range(num_game_updates):
        # Render same frame multiple times for slower movement
        frame = game.get_frame()
        for _ in range(frames_per_update):
            frames.append(frame)
        game.update()

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
    print("Simulating Pong game...")
    # 480 game updates at 6fps = 80 seconds total
    # Ball moves 1 cell every ~167ms (very slow, easy to watch)
    frames = simulate_pong_game(num_game_updates=480, frames_per_update=1)
    print(f"Generated {len(frames)} frames")

    print("Creating contribution graph SVG...")
    svg_content = create_contribution_svg(frames, fps=6)

    with open('pong-contribution.svg', 'w') as f:
        f.write(svg_content)

    print("Generated pong-contribution.svg")
