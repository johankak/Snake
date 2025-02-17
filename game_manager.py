import json
import random
from tkinter import Tk, Canvas, Label
from PIL import Image, ImageTk
from constants import *
from snake import Snake
from food import Food, BadFood, SpeedFood, SlowFood, ReverseFood

class GameManager:
    def __init__(self):
        self.window = Tk()
        self.window.title("Snake")
        self.window.resizable(False, False)
        
        self.score = 0
        self.level = 1
        self.current_speed = SPEED
        self.is_speed_boosted = False
        self.is_slowed = False
        
        self.label = Label(self.window, text="Score:0  Level:1", font=('consolas', 40))
        self.label.pack()
        
        self.canvas = Canvas(
            self.window,
            bg=BACKGROUND_COLOR,
            height=GAME_HEIGHT,
            width=GAME_WIDTH
        )
        self.canvas.pack()
        
        self.setup_window()
        self.bind_keys()
        
        self.snake = None
        self.food = None
        self.bad_food = None
        self.speed_food = None
        self.slow_food = None
        self.reverse_food = None
        
        self.show_start_menu()

    def setup_window(self):
        self.window.update()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def bind_keys(self):
        self.window.bind('<Left>', lambda e: self.snake.change_direction('left'))
        self.window.bind('<Right>', lambda e: self.snake.change_direction('right'))
        self.window.bind('<Up>', lambda e: self.snake.change_direction('up'))
        self.window.bind('<Down>', lambda e: self.snake.change_direction('down'))
        self.window.bind('<space>', self.start_game)
    
    def save_score(self):
        try:
            with open('last_score.json', 'w') as f:
                json.dump({'last_score': self.score}, f)
        except:
            pass
    
    def load_score(self):
        try:
            with open('last_score.json', 'r') as f:
                data = json.load(f)
                return data.get('last_score', 0)
        except:
            return 0
    
    def show_start_menu(self):
        self.canvas.delete("all")
        
        try:
            snake_image = Image.open("snake_image.png")
            snake_image = snake_image.resize((200, 200))
            snake_photo = ImageTk.PhotoImage(snake_image)
            
            self.canvas.create_image(
                GAME_WIDTH // 2,
                GAME_HEIGHT // 5,
                image=snake_photo,
                tag="snake_image"
            )
            self.canvas.image = snake_photo
        except:
            print("Could not load snake_image.png")
        
        self.canvas.create_text(
            GAME_WIDTH // 2,
            GAME_HEIGHT // 3,
            text="SNAKE",
            fill="green",
            font=('consolas', 60, 'bold')
        )
        
        last_score = self.load_score()
        self.canvas.create_text(
            GAME_WIDTH // 2,
            GAME_HEIGHT // 2,
            text=f"Last Score: {last_score}",
            fill="white",
            font=('consolas', 40)
        )
        
        self.canvas.create_text(
            GAME_WIDTH // 2,
            GAME_HEIGHT * 2 // 3,
            text="Press SPACE to Play",
            fill="yellow",
            font=('consolas', 40)
        )
    
    def start_game(self, event=None):
        self.canvas.delete("all")
        self.score = 0
        self.level = 1
        self.current_speed = SPEED
        self.is_speed_boosted = False
        self.is_slowed = False
        
        self.label.config(text="Score:0  Level:1")
        
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.bad_food = None
        self.speed_food = None
        self.slow_food = None
        self.reverse_food = None
        
        self.next_turn()
    
    def update_level(self):
        new_level = (self.score // 10) + 1
        
        if new_level > self.level:
            self.level = new_level
            if not self.is_slowed and not self.is_speed_boosted:
                base_reduction = 80
                self.current_speed = max(SPEED - (base_reduction * (self.level - 1)), 50)
            
            self.label.config(text=f"Score:{self.score}  Level:{self.level}")
    
    def end_speed_boost(self):
        self.is_speed_boosted = False
    
    def end_slow_boost(self):
        self.is_slowed = False
    
    def game_over(self):
        self.save_score()
        self.canvas.create_text(
            GAME_WIDTH // 2,
            GAME_HEIGHT // 2,
            text="GAME OVER",
            fill="red",
            font=('consolas', 40)
        )
        self.window.after(1000, self.show_start_menu)
    
    def next_turn(self):
        head_pos = self.snake.move()
        
        if self.snake.check_collision():
            self.game_over()
            return

        #kolize s normalnim jidlem
        if self.food and head_pos[0] == self.food.coordinates[0] and head_pos[1] == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"Score:{self.score}  Level:{self.level}")
            self.canvas.delete("food")
            self.food = Food(self.canvas)
            self.snake.grow()

        #kolize se spatnym jidlem
        if self.bad_food and head_pos[0] == self.bad_food.coordinates[0] and head_pos[1] == self.bad_food.coordinates[1]:
            self.score -= 1
            self.label.config(text=f"Score:{self.score}  Level:{self.level}")
            self.canvas.delete("bad_food")
            self.bad_food = None
            self.snake.shrink()

        #kolize s rychlovacim jidlem
        if self.speed_food and head_pos[0] == self.speed_food.coordinates[0] and head_pos[1] == self.speed_food.coordinates[1]:
            self.is_speed_boosted = True
            self.label.config(text=f"Score:{self.score}  Level:{self.level}")
            self.canvas.delete("speed_food")
            self.speed_food = None
            self.window.after(SPEED_BOOST_DURATION, self.end_speed_boost)

        #kolize se zpomalovacim jidlem
        if self.slow_food and head_pos[0] == self.slow_food.coordinates[0] and head_pos[1] == self.slow_food.coordinates[1]:
            self.is_slowed = True
            self.label.config(text=f"Score:{self.score}  Level:{self.level}")
            self.canvas.delete("slow_food")
            self.slow_food = None
            self.window.after(SLOW_BOOST_DURATION, self.end_slow_boost)

        #kolize s reverse jidlem
        if self.reverse_food and head_pos[0] == self.reverse_food.coordinates[0] and head_pos[1] == self.reverse_food.coordinates[1]:
            self.snake.reverse_direction()
            self.label.config(text=f"Score:{self.score}  Level:{self.level}")
            self.canvas.delete("reverse_food")
            self.reverse_food = None

        #generovani jidla
        if not self.bad_food and random.randint(1, 100) <= 10:
            self.bad_food = BadFood(self.canvas, self.window)

        if not self.speed_food and random.randint(1, 400) <= 5:
            self.speed_food = SpeedFood(self.canvas, self.window)

        if not self.slow_food and random.randint(1, 400) <= 5:
            self.slow_food = SlowFood(self.canvas, self.window)

        if not self.reverse_food and random.randint(1, 400) <= 5:
            self.reverse_food = ReverseFood(self.canvas, self.window)

        self.update_level()

        #urceni aktualni rychlsoti, podle posledniho sebraneho efektu
        if self.is_speed_boosted and self.is_slowed:
            if self.window.getvar('last_effect') == 'speed':
                self.current_speed = BOOSTED_SPEED
            else:
                self.current_speed = SLOWED_SPEED
        elif self.is_speed_boosted:
            self.current_speed = BOOSTED_SPEED
        elif self.is_slowed:
            self.current_speed = SLOWED_SPEED
        else:
            base_reduction = 80
            self.current_speed = max(SPEED - (base_reduction * (self.level - 1)), 50)
        
        #naplanovani dalsiho tahu
        self.window.after(self.current_speed, self.next_turn)
        
    
    def run(self):
        self.window.mainloop()