""" class for background in air hockey game """
import pygame

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (0, 128, 128)  # Teal background color
        self.line_color = (255, 255, 255)  # White lines
    
    def update(self):
        # For now, no update logic is needed for the background
        pass