from tkinter import Canvas
import random
from constants import *

class FoodBase: #rodicovska trida
    def __init__(self, canvas: Canvas, color: str, tag: str):
        self.canvas = canvas
        self.coordinates = self._generate_coordinates()
        self.canvas.create_oval(
            self.coordinates[0], self.coordinates[1],
            self.coordinates[0] + SPACE_SIZE,
            self.coordinates[1] + SPACE_SIZE,
            fill=color, tag=tag
        )
    
    def _generate_coordinates(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        return [x, y]

class Food(FoodBase):
    def __init__(self, canvas: Canvas):
        super().__init__(canvas, FOOD_COLOR, "food") #super umoznuje pristupovat k metodam rodicu

class BadFood(FoodBase):
    def __init__(self, canvas: Canvas, window):
        super().__init__(canvas, BAD_FOOD_COLOR, "bad_food")
        self.window = window
        self.window.after(BAD_FOOD_LIFETIME, self.remove)
    
    def remove(self):
        self.canvas.delete("bad_food")

class SpeedFood(FoodBase):
    def __init__(self, canvas: Canvas, window):
        super().__init__(canvas, SPEED_FOOD_COLOR, "speed_food")
        self.window = window
        self.window.after(SPEED_FOOD_LIFETIME, self.remove)
    
    def remove(self):
        self.canvas.delete("speed_food")

class SlowFood(FoodBase):
    def __init__(self, canvas: Canvas, window):
        super().__init__(canvas, SLOW_FOOD_COLOR, "slow_food")
        self.window = window
        self.window.after(SLOW_FOOD_LIFETIME, self.remove)
    
    def remove(self):
        self.canvas.delete("slow_food")

class ReverseFood(FoodBase):
    def __init__(self, canvas: Canvas, window):
        super().__init__(canvas, "orange", "reverse_food")
        self.window = window
        self.window.after(5000, self.remove)
    
    def remove(self):
        self.canvas.delete("reverse_food")