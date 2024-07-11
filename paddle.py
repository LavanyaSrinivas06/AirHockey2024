"""Class for paddle object in airhockey game"""
import pygame
import config

class Paddle: 
    #position of paddle
    #dimensions of paddle
    #color of paddle
    #Speed of paddle
    #direction of paddle
    #screen width and height

    #initialize the paddle object
    def__init__(self, x, y, width, height, color, speed, screen_width, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.direction = 0
        self.vx = 0
        self.vy = 0
        self.screen_width = screen_width
        self.screen_height = screen_height