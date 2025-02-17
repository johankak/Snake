from tkinter import Canvas
from constants import *

class Snake:
    def __init__(self, canvas: Canvas): #import canvas pro vykresleni
        self.canvas = canvas 
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.direction = 'down'  #pocatecni smer pohybu
        
        #vytvoreni pocatecniho tela hada
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
            
        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(
                x, y, 
                x + SPACE_SIZE, 
                y + SPACE_SIZE, 
                fill=SNAKE_COLOR, 
                tag="snake"
            )
            self.squares.append(square)
    
    def change_direction(self, new_direction): #meni smer pohybu
#zabranuje otoceni o 180 stupnu
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def reverse_direction(self):
#obrati smer hada o 180 stupnu, po sezrani reverse jidla...
        if self.direction == 'up':
            self.direction = 'down'
        elif self.direction == 'down':
            self.direction = 'up'
        elif self.direction == 'left':
            self.direction = 'right'
        elif self.direction == 'right':
            self.direction = 'left'

    def move(self):
#pohyb hada - princip pridavani nove hlavy na zacatek tela a odstraneni posledni casti
        x, y = self.coordinates[0]
        
        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE
            
        #vlozeni hlavy
        self.coordinates.insert(0, [x, y])
        
        #vytvoreni noveho ctverce pro hlavu
        square = self.canvas.create_rectangle(
            x, y, 
            x + SPACE_SIZE, 
            y + SPACE_SIZE, 
            fill=SNAKE_COLOR
        )
        self.squares.insert(0, square)
        
        #odstraneni posledniho segmentu, pokud se had neprodlouzil
        if len(self.coordinates) > self.body_size:
            del self.coordinates[-1]
            self.canvas.delete(self.squares[-1])
            del self.squares[-1]
            
        return self.coordinates[0]
    
    def grow(self): #zvetseni hada
        self.body_size += 1
    
    def shrink(self): #zmenseni hada
        if len(self.coordinates) > 1:
            self.body_size -= 1
            del self.coordinates[-1]
            self.canvas.delete(self.squares[-1])
            del self.squares[-1]
    
    def check_collision(self): #kontrola kolizi
        x, y = self.coordinates[0]
        
        #kolize se stenami
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
            
        #kolize s vlastnim telem
        for body_part in self.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True
                
        return False
