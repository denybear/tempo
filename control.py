#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 Denybear
#
# SPDX-License-Identifier: MIT

"""
Receive messages from the input port and print them out.
"""
import sys
#from controlDisplay import display_grid
import pygame

def display_grid(text_list, top_label="NOW PLAYING", active_cell=-1):
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

    # Fonts
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Grid Viewer")
    font_label = pygame.font.SysFont("Arial", 40)
    font_cells = pygame.font.SysFont("Arial", 22)

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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(white)

        # Draw top label
        label_surface = font_label.render(top_label, True, black)
        screen.blit(label_surface, label_surface.get_rect(center=(width // 2, label_height // 2)))

        # Draw grid
        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                x = col * (cell_width + gap) + gap
                y = row * (cell_height + gap) + gap + label_height

                bg_color = red if index == active_cell else gray
                text_color = white_text if index == active_cell else black

                # Draw cell
                rect = pygame.Rect(x, y, cell_width, cell_height)
                pygame.draw.rect(screen, bg_color, rect)

                # Wrap and center text
                cell_text = text_list[index] if index < len(text_list) else ""
                lines = wrap_text(cell_text, font_cells, max_text_width)
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






# Playlist definition
playList = [
	{"song":"Papa was a rolling stone", "artist":"Temptations", "bpm":110},
	{"song":"I don't want a lover", "artist":"Texas", "bpm":120}
]


# main loop

# Build text list from playlist
texts = []
for i in range (len(playList)):
	texts.append (playList [i]["song"])

# Set label and active cell index
highlighted_cell = 0  # e.g. highlight cell 24 (0-based index)
top_banner = "PLAYING: " + playList [highlighted_cell]["song"] + " / " + playList [highlighted_cell]["artist"]
# Call the function
display_grid(texts, top_label=top_banner, active_cell=highlighted_cell)

# Set label and active cell index
highlighted_cell = 1  # e.g. highlight cell 24 (0-based index)
top_banner = "PLAYING: " + playList [highlighted_cell]["song"] + " / " + playList [highlighted_cell]["artist"]
# Call the function
display_grid(texts, top_label=top_banner, active_cell=highlighted_cell)
