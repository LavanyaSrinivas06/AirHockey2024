import pygame
import config
 
class Puck:
    def __init__(self, x, y, radius, color, initial_speed):
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.radius = radius
        self.color = color
        self.vx = initial_speed  
        self.vy = initial_speed  
        self.started = False
 
    def start(self):
        self.vx = config.PUCK_INITIAL_SPEED
        self.vy = config.PUCK_INITIAL_SPEED
        self.started = True
 
    def update(self, screen_width, screen_height):
        if self.started:
            self.x += self.vx
            self.y += self.vy
 
            
            if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
                self.vx = -self.vx
 
            if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
                self.vy = -self.vy
 
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
 
    def check_collision_with_paddle(self, paddle):
        if (
            self.x + self.radius > paddle.x
            and self.x - self.radius < paddle.x + paddle.width
            and self.y + self.radius > paddle.y
            and self.y - self.radius < paddle.y + paddle.height
        ):
            # Determine the overlap distance
            overlap_x_left = self.x + self.radius - paddle.x
            overlap_x_right = paddle.x + paddle.width - self.x + self.radius
            overlap_y_top = self.y + self.radius - paddle.y
            overlap_y_bottom = paddle.y + paddle.height - self.y + self.radius
 
            if min(overlap_x_left, overlap_x_right) < min(overlap_y_top, overlap_y_bottom):
                # Horizontal collision
                self.vx = -self.vx * config.PUCK_SPEED_INCREASE
                if overlap_x_left < overlap_x_right:
                    self.x = paddle.x - self.radius
                else:
                    self.x = paddle.x + paddle.width + self.radius
            else:
                # Vertical collision
                self.vy = -self.vy * config.PUCK_SPEED_INCREASE
                if overlap_y_top < overlap_y_bottom:
                    self.y = paddle.y - self.radius
                else:
                    self.y = paddle.y + paddle.height + self.radius
 
            # Adjust the puck's velocity based on the paddle's movement
            self.vx += paddle.vx * 0.5
            self.vy += paddle.vy * 0.5
            return True
        return False
 
    def reset(self, x=None, y=None):
        if x is None:
            x = self.initial_x
        if y is None:
            y = self.initial_y
        self.x = x
        self.y = y
        self.vx = config.PUCK_INITIAL_SPEED
        self.vy = config.PUCK_INITIAL_SPEED
        self.started = False