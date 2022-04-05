import random
import sys
import pygame
from pygame.color import THECOLORS

# TODO(1) Отрисовать лабиринт
# TODO(2) Добавить игрока и реализовать его перемещение
# TODO(3) Добавить выход и условие победы
# TODO(4) Добавить ключи

MAZE_MAP = [
    '#######@#####',
    '#  K#     #K#',
    '# ### # # # #',
    '# #   # #   #',
    '# # # #######',
    '# # #       #',
    '# # ####### #',
    '# #     #K# #',
    '# ##### # # #',
    '#   #   # # #',
    '### # ### # #',
    '#     #     #',
    '#X###########',
]

BLOCK_SIDE = 64
CELL_SIDE = 64
WIDTH = len(MAZE_MAP[0])
HEIGHT = len(MAZE_MAP)

SCREEN_WIDTH = WIDTH * BLOCK_SIDE
SCREEN_HEIGHT = HEIGHT * BLOCK_SIDE

wall_textures = []
for i in range(0, 16):
    wall_textures.append(pygame.image.load(f'img/wall_64x64_{i}.png'))

key_texture = pygame.image.load(f'img/key.png')
door_textures = []
for i in range(4):
    door_textures.append(pygame.image.load(f'img/door{i}.png'))
player_texture = pygame.image.load(f'img/player.png')


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('arial', 60)
text = font.render('You Win!', True, THECOLORS['green'])


class Wall:
    def __init__(self, x, y, texture):
        # TODO(1.1) Атрибуты блока стены:
        self.x = x
        self.y = y
        self.texture = texture

    def draw(self):
        # TODO(1.2) Отобразить блок.
        screen.blit(self.texture, (self.x,self.y))


class Key:
    def __init__(self, x, y, cell, texture):
        # TODO(4.1) Создать атрибуты ключа:
        self.x = x
        self.y = y
        self.cell = cell
        self.texture = texture 
        self.is_taken = False

    def draw(self):
        if not self.is_taken:
            screen.blit(self.texture, (self.x, self.y))


class Exit:
    def __init__(self, x, y, cell, textures):
       self.x = x
       self.y = y
       self.cell = cell
       self.textures = textures
       self.keys = 0

    def draw(self):
        screen.blit(self.textures[self.keys], (self.x,self.y))

class Maze:
    def __init__(self):
        self.walls = []
        self.player = Player(0,0)
        self.exit = Exit(0, 0, 0, door_textures)
        self.keys = []
        
        for i in range(len(MAZE_MAP)):
            for j in range(len(MAZE_MAP[i])):
                if MAZE_MAP[i][j] == "#":
                    self.walls.append(Wall(j * BLOCK_SIDE,
                                           i * CELL_SIDE,
                                           random.choice(wall_textures)))
                elif MAZE_MAP[i][j] == "@":
                    self.player.x = j*BLOCK_SIDE
                    self.player.y = i * CELL_SIDE
                elif MAZE_MAP[i][j] == "X":
                    self.exit.x = j * BLOCK_SIDE
                    self.exit.y = i * CELL_SIDE
                elif MAZE_MAP[i][j] == "K":
                    self.keys.append(Key(j * BLOCK_SIDE,
                                           i * CELL_SIDE,
                                           0,
                                           key_texture))

    def move_player(self):
        self.set_player_direction(self.player.direction)
        self.player.move()
        
        for key in self.keys:
            if key.x == self.player.x and key.y == self.player.y and not key.is_taken:
                key.is_taken = True
                self.exit.keys += 1
                
        
    def set_player_direction(self, direction):
        if self.player_can_move(direction):
            self.player.direction = direction
        else:
            self.player.direction = Direction.NONE

    def player_can_move(self, direction):
        pcx, pcy = self.get_player_cell()
        if direction == Direction.UP:
            pcy -= 1
        elif direction == Direction.DOWN:
            pcy +=1
        elif direction == Direction.LEFT:
            pcx -= 1
        elif direction == Direction.RIGHT:
            pcx +=1
        if pcx < 13 and pcy < 13 and MAZE_MAP [pcy][pcx]=="#":
            return False
        return True

    def draw(self):
        for wall in self.walls:
            wall.draw()
            self.player.draw()
            self.exit.draw()
            for key in self.keys:
                key.draw()


    def win(self):
        return self.player.x == self.exit.x and self.player.y == self.exit.y and self.exit.keys == 3
                    

    def get_player_cell(self):
        return (self.player.x // CELL_SIDE, self.player.y // CELL_SIDE)


class Direction:
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Player:
    def __init__(self, x, y):
        # TODO(2.1) Создать атрибуты игрока:
        self.x = x
        self.y = y
        self.texture = player_texture
        self.step = CELL_SIDE
        self.direction = Direction.NONE
        

    def draw(self):
        # TODO(2.2) Отобразить игрока
        screen.blit(self.texture, (self.x, self.y))

    def move(self):
        # TODO(2.3) Реализовать движение игрока.
        if self.direction == Direction.UP:
            self.y -= self.step
        elif self.direction == Direction.DOWN:
            self.y += self.step
        elif self.direction == Direction.LEFT:
            self.x -= self.step
        elif self.direction == Direction.RIGHT:
            self.x += self.step


def start_level():
    maze = Maze()

    while True:
        if maze.win():
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    maze.set_player_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    maze.set_player_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    maze.set_player_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    maze.set_player_direction(Direction.RIGHT)
            elif event.type == pygame.KEYUP:
                maze.set_player_direction(Direction.NONE)

        maze.move_player()

        screen.fill((0, 0, 0))
        maze.draw()

        pygame.display.flip()
        pygame.time.wait(66)


def show_win_message():
    screen.blit(text, (CELL_SIDE * 2, SCREEN_HEIGHT - CELL_SIDE - 60))
    pygame.display.flip()
    pygame.time.wait(1000)


while True:
    start_level()
    show_win_message()
