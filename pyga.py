import pygame
import time

pygame.init()

# Grid configuration
rows, cols = 8, 8
cell_width = 160
cell_height = 80
gap = 10
label_height = 60
max_text_width = 140
width = cols * cell_width + (cols + 1) * gap
height = rows * cell_height + (rows + 1) * gap + label_height

# Colors
white = (255, 255, 255)
gray = (200, 200, 200)
black = (0, 0, 0)
red = (220, 0, 0)
white_text = (255, 255, 255)

# Text content
text_list = [
    "Short",
    "Text that needs to be wrapped into multiple lines because it exceeds the allowed width",
    "Python",
    "Another example with centered multiline content in one cell",
    "Quick brown fox jumps over the lazy dog several times today",
    "Pygame rocks!",
    "This one is short",
    "Wrapping works great in cells"
] * 8  # 64 entries

# Fonts
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Resetting Cell Grid")
font_label = pygame.font.SysFont("Arial", 40)
font_cells = pygame.font.SysFont("Arial", 22)

# Wrap text by pixel width
def wrap_text(text, font, max_pixel_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if font.size(test_line)[0] <= max_pixel_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# Counter setup
counter = 0
last_update_time = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Timer-based increment every 3 seconds
    current_time = time.time()
    if current_time - last_update_time >= 3:
        counter = (counter + 1) % len(text_list)  # Loop through cells
        last_update_time = current_time

    screen.fill(white)

    # Top label
    label = font_label.render("NOW PLAYING", True, black)
    screen.blit(label, label.get_rect(center=(width // 2, label_height // 2)))

    # Draw grid
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            x = col * (cell_width + gap) + gap
            y = row * (cell_height + gap) + gap + label_height

            # Cell style logic
            if index == counter:
                bg_color = red
                text_color = white_text
            else:
                bg_color = gray
                text_color = black

            # Draw cell
            rect = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, bg_color, rect)

            # Wrap and center text
            lines = wrap_text(text_list[index], font_cells, max_text_width)
            line_height = font_cells.get_linesize()
            total_text_height = len(lines) * line_height
            text_y_start = y + (cell_height - total_text_height) // 2

            for i, line in enumerate(lines):
                rendered_line = font_cells.render(line, True, text_color)
                line_rect = rendered_line.get_rect()
                line_rect.centerx = x + cell_width // 2
                line_rect.y = text_y_start + i * line_height
                screen.blit(rendered_line, line_rect)

    pygame.display.flip()

pygame.quit()
