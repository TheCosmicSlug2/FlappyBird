import pygame as pg
from random import randint
from math import sqrt
import textures
import sys


class Player:
    def __init__(self, posx, posy, flap_strength, gravity):
        self.posx = posx
        self.posy = posy
        self.flap_strength = flap_strength
        self.y_velocity = 0
        self.gravity = gravity
        self.velocity_boundaries = (-8, 10)
        self.dims = (20, 20)
        self.angle = 0
        self.max_up_angle = 25   # Angle maximum pour la montée
        self.max_down_angle = -60  # Angle maximum pour la descente
        self.angle_speed = 2

    def flap(self):
        self.y_velocity -= self.flap_strength
        if self.y_velocity < self.velocity_boundaries[0]:
            self.y_velocity = self.velocity_boundaries[0]
        if self.y_velocity > self.velocity_boundaries[1]:
            self.y_velocity = self.velocity_boundaries[1]
        global bird_flap_tick  # Utiliser la variable globale pour le tick de flap
        bird_flap_tick = 0  # Réinitialiser le tick après chaque flap

    def check_ground_collision(self):
        return self.posy + self.dims[1] > RES[1]

    def update(self):
        self.y_velocity += self.gravity
        self.posy += self.y_velocity

        # Ajuster l'angle en fonction de la vélocité

        if self.y_velocity > 0:
            self.angle = max(self.angle - self.angle_speed, self.max_down_angle)
        else:
            self.angle = min(self.angle + self.angle_speed, self.max_up_angle)

    def get_rect(self):
        return pg.Rect(self.posx, self.posy, self.dims[0], self.dims[1])

    @staticmethod
    def get_sprite(flap=False):
        if flap:
            return dic_textures["yellowbird_upflap"]

        return dic_textures["yellowbird_midflap"]


class Pipe:
    def __init__(self, posx, gap_top_posy, gap_height):
        self.posx = posx
        self.gap_top_posy = gap_top_posy
        self.gap_height = gap_height
        self.width = pipe_size[0]
        self.bottom_height = self.gap_top_posy + self.gap_height
        self.top_sprite, self.bottom_sprite = self.get_sprite()
        self.behind_player = False

    def check_out_of_screen(self):
        if self.posx + self.width < 0:
            self.__init__(posx=RES[0], gap_top_posy=randint(40, 340), gap_height=randint(80, 140))

    def move_left(self):
        self.posx -= 5
        self.check_out_of_screen()

    def get_sprite(self) -> tuple[pg.Surface, pg.Surface]:
        top_height = self.gap_top_posy
        bottom_height = RES[1] - (top_height + self.gap_height)

        up_pipe_top_left_corner_y = top_height - pipe_size[1]
        raw_top_pipe = dic_textures["bottom_pipe"]
        raw_bottom_pipe = dic_textures["top_pipe"]

        resized_top_sprite = pg.Surface((self.width, self.gap_top_posy), pg.SRCALPHA)
        resized_top_sprite.blit(raw_top_pipe, (0, up_pipe_top_left_corner_y))

        bottom_sprite = pg.Surface((self.width, bottom_height), pg.SRCALPHA)
        bottom_sprite.blit(raw_bottom_pipe, (0, 0))

        return resized_top_sprite, bottom_sprite

    def get_rects(self):
        top_rect = pg.Rect(self.posx, 0, self.width, self.gap_top_posy)
        bottom_rect = pg.Rect(self.posx, self.gap_top_posy + self.gap_height, self.width, RES[1] - (self.gap_top_posy + self.gap_height))
        return top_rect, bottom_rect


def get_space_pressed():
    keys = pg.key.get_pressed()
    return keys[pg.K_SPACE]


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pg.init()
RES = (800, 600)
SCREEN = pg.display.set_mode(RES)
pg.display.set_caption("FlappyBird - AI")
clock = pg.time.Clock()
FPS = 30

nb_size = (20, 40)
bg_size = RES
bird_size = (34*1.5, 24*1.5)
pipe_size = (80, RES[1])

liste_texture_name = [
    ("0", nb_size),
    ("1", nb_size),
    ("2", nb_size),
    ("3", nb_size),
    ("4", nb_size),
    ("5", nb_size),
    ("6", nb_size),
    ("7", nb_size),
    ("8", nb_size),
    ("9", nb_size),
    ("background_day", bg_size),
    ("yellowbird_downflap", bird_size),
    ("yellowbird_midflap", bird_size),
    ("yellowbird_upflap", bird_size),
    ("bottom_pipe", pipe_size),
    ("top_pipe", pipe_size)
]

dic_textures = textures.load_textures(liste_texture_name)

bird = Player(
    posx=80,
    posy=RES[1] // 2,
    flap_strength=10,
    gravity=0.5
)
pipe = Pipe(
    posx=RES[0], gap_top_posy=randint(40, 340), gap_height=randint(80, 140)
)

bird_sprite = bird.get_sprite()
bird_flap_tick = 0
bird_flapped = False
space_pressed = False
score = 0
running = True

while running:
    SCREEN.blit(dic_textures["background_day"], (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYUP:
            space_pressed = False

    if get_space_pressed() and not space_pressed:
        bird_sprite = bird.get_sprite(flap=True)
        bird_flapped = True
        bird.flap()
        space_pressed = True

    if bird_flapped and bird_flap_tick > 5:
        bird_sprite = bird.get_sprite(flap=False)
        bird_flapped = False

    bird.update()
    pipe.move_left()

    if bird.check_ground_collision():
        running = False

    bird_rect = bird.get_rect()
    pipe_top_rect, pipe_bottom_rect = pipe.get_rects()

    if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
        print("Collision detected")
        running = False

    if bird.posx > (pipe.posx + pipe.width) // 2 and not pipe.behind_player:
        score += 1
        pipe.behind_player = True
        print(score)

    # Rotation de l'oiseau
    rotated_bird_sprite = pg.transform.rotate(bird_sprite, bird.angle)
    rotated_bird_rect = rotated_bird_sprite.get_rect(center=(bird.posx + bird.dims[0] // 2, bird.posy + bird.dims[1] // 2))

    SCREEN.blit(pipe.top_sprite, (pipe.posx, 0))
    SCREEN.blit(pipe.bottom_sprite, (pipe.posx, pipe.gap_top_posy + pipe.gap_height))
    SCREEN.blit(rotated_bird_sprite, rotated_bird_rect.topleft)

    pg.display.update()
    clock.tick(FPS)
    bird_flap_tick += 1
