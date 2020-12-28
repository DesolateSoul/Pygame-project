from pygame import *
import pygame
import pyganim
import random

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
DISPLAY = (WINDOW_WIDTH, WINDOW_HEIGHT)
BACKGROUND_COLOR = "#000000"
FPS = 60

MOVE_SPEED = 14
WIDTH = 52  # Размеры игрока
HEIGHT = 64
COLOR = "#888888"
JUMP_POWER = 20
GRAVITY = 0.7

PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 64

ANIMATION_RIGHT = [('data/run1.png', 0.1), ('data/run2.png', 0.1), ('data/run3.png', 0.1), ('data/run4.png', 0.1),
                   ('data/run5.png', 0.1), ('data/run6.png', 0.1)]
ANIMATION_LEFT = [('data/lrun1.png', 0.1), ('data/lrun2.png', 0.1), ('data/lrun3.png', 0.1), ('data/lrun4.png', 0.1),
                  ('data/lrun5.png', 0.1), ('data/lrun6.png', 0.1)]
ANIMATION_JUMP_LEFT = [('data/ljump1.png', 0.2), ('data/ljump2.png', 0.2), ('data/ljump3.png', 0.2),
                       ('data/ljump4.png', 0.2), ('data/ljump5.png', 0.2), ('data/ljump6.png', 0.2)]
ANIMATION_JUMP_RIGHT = [('data/jump1.png', 0.2), ('data/jump2.png', 0.2), ('data/jump3.png', 0.2),
                        ('data/jump4.png', 0.2), ('data/jump5.png', 0.2), ('data/jump6.png', 0.2)]
ANIMATION_STAY_RIGHT = [('data/idle1.png', 0.2), ('data/idle2.png', 0.2), ('data/idle3.png', 0.2),
                        ('data/idle4.png', 0.2)]
ANIMATION_STAY_LEFT = [('data/lidle1.png', 0.2), ('data/lidle2.png', 0.2), ('data/lidle3.png', 0.2),
                       ('data/lidle4.png', 0.2)]


class Player(sprite.Sprite):
    def __init__(self, x, y, move_left, move_right, move_up, gaze_direction="right"):
        sprite.Sprite.__init__(self)
        self.start_pos_x = x
        self.start_pos_y = y
        # Переменные отвечающие за движение
        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.x_speed = 0
        self.y_speed = 0
        self.ground_touch = False

        self.gaze_direction = gaze_direction  # Направление взгляда
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        #  Анимация движения вправо
        self.animation_run_right = pyganim.PygAnimation(ANIMATION_RIGHT)
        self.animation_run_right.play()
        #  Анимация движения влево
        self.animation_run_left = pyganim.PygAnimation(ANIMATION_LEFT)
        self.animation_run_left.play()
        #  Анимация бездействия
        self.animation_stay_right = pyganim.PygAnimation(ANIMATION_STAY_RIGHT)
        self.animation_stay_right.play()
        #  Анимация прыжка влево
        self.animation_jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.animation_jump_left.play()
        #  Анимация прыжка вправо
        self.animation_jump_right = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.animation_jump_right.play()

        self.animation_stay_left = pyganim.PygAnimation(ANIMATION_STAY_LEFT)
        self.animation_stay_left.play()

        self.animation_run_right.scale((WIDTH, HEIGHT))
        self.animation_run_left.scale((WIDTH, HEIGHT))
        self.animation_stay_right.scale((WIDTH, HEIGHT))
        self.animation_jump_left.scale((WIDTH, HEIGHT))
        self.animation_jump_right.scale((WIDTH, HEIGHT))
        self.animation_stay_left.scale((WIDTH, HEIGHT))

        self.animation_stay_right.blit(self.image, (0, 0))  # По-умолчанию, стоим

    def update(self, left, right, up, platforms):
        if up:
            if self.ground_touch:  # Прыгаем, только когда можем оттолкнуться от земли
                self.y_speed = -JUMP_POWER
            if self.gaze_direction == "right":
                self.image.fill(Color(COLOR))
                self.animation_jump_right.blit(self.image, (0, 0))
            elif self.gaze_direction == "left":
                self.image.fill(Color(COLOR))
                self.animation_jump_left.blit(self.image, (0, 0))
        if left:
            self.gaze_direction = "left"
            self.x_speed = -MOVE_SPEED
            self.image.fill(Color(COLOR))
            if up:
                self.animation_jump_left.blit(self.image, (0, 0))
            else:
                self.animation_run_left.blit(self.image, (0, 0))
        if right:
            self.gaze_direction = "right"
            self.x_speed = MOVE_SPEED
            self.image.fill(Color(COLOR))
            if up:
                self.animation_jump_right.blit(self.image, (0, 0))
            else:
                self.animation_run_right.blit(self.image, (0, 0))
        if not (left or right):  # Стоим, когда нет указаний идти
            self.x_speed = 0
            if not up and self.ground_touch:
                if self.gaze_direction == "right":
                    self.image.fill(Color(COLOR))
                    self.animation_stay_right.blit(self.image, (0, 0))
                elif self.gaze_direction == "left":
                    self.image.fill(Color(COLOR))
                    self.animation_stay_left.blit(self.image, (0, 0))
        if not self.ground_touch:  # изменение скорости в зависимости от гравитации
            self.y_speed += GRAVITY

        self.ground_touch = False
        self.rect.y += self.y_speed  # Изменение положения квадрата игрока
        self.collide(0, self.y_speed, platforms)  # Проверка столкновений
        self.rect.x += self.x_speed  # Изменение положения квадрата игрока
        self.collide(self.x_speed, 0, platforms)  # Проверка столкновений

    def collide(self, x_speed, y_speed, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                if x_speed > 0:
                    self.rect.right = platform.rect.left
                if x_speed < 0:
                    self.rect.left = platform.rect.right
                if y_speed > 0:
                    self.rect.bottom = platform.rect.top
                    self.ground_touch = True
                    self.y_speed = 0
                if y_speed < 0:
                    self.rect.top = platform.rect.bottom
                    self.y_speed = 0


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)  # Квадрат по которому перемещается камера

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    g, t, _, _ = target_rect
    _, _, w, h = camera
    g, t = -g + WINDOW_WIDTH / 2, -t + WINDOW_HEIGHT / 2

    g = min(0, g)                           # Не движемся дальше левой границы
    g = max(-(camera.width - WINDOW_WIDTH), g)   # Не движемся дальше правой границы
    t = max(-(camera.height - WINDOW_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы
    return Rect(g, t, w, h)


def generate_level(filename):
    with open(f"data/{filename}", mode="w", encoding="utf-8") as generated_level:
        for i in range(32):
            for k in range(64):
                if i == 0 or i == 31:
                    print("-", end="", file=generated_level)
                    if k == 63:
                        print("", file=generated_level)
                elif k == 0:
                    print("-", end="", file=generated_level)
                elif k == 63:
                    print("-", file=generated_level)
                else:
                    print("", end=" ", file=generated_level)
    with open(f"data/{filename}", mode="r", encoding="utf-8") as generated_level:
        level = generated_level.read().splitlines()
    for i in range(len(level[1:-1])):
        n = random.randint(1, len(level[0][1:-1]) - 7)
        for k in range(7):
            level[i + 1] = level[i + 1][:n + k] + "-" + level[i + 1][n + k + 1:]
    return level


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("data/platform.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Платформер")
    bg = image.load("data/background.png")
    bg = pygame.transform.scale(bg, (4096, 2048))
    timer = pygame.time.Clock()

    main_character = Player(600, 900, False, False, False)
    objects = pygame.sprite.Group()  # Все объекты
    objects.add(main_character)
    platforms = []

    level = generate_level("level.txt")
    x = y = 0  # координаты установки платформ
    for line in level:
        for symbol in line:
            if symbol == "-":
                platform = Platform(x, y)
                objects.add(platform)
                platforms.append(platform)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Получившаяся длина уровня,
    total_level_height = len(level) * PLATFORM_HEIGHT  # высота
    camera = Camera(camera_configure, total_level_width, total_level_height)

    running = True
    while running:  # Основной игровой цикл
        timer.tick(FPS)
        screen.blit(bg, (camera_configure(camera.state, main_character.rect).x,
                         camera_configure(camera.state, main_character.rect).y))  # Перерисовка фона
        for ev3nt in pygame.event.get():
            if ev3nt.type == QUIT:
                running = False

            if ev3nt.type == KEYDOWN and ev3nt.key == K_UP:
                main_character.move_up = True
            if ev3nt.type == KEYUP and ev3nt.key == K_UP:
                main_character.move_up = False

            if ev3nt.type == KEYDOWN and ev3nt.key == K_LEFT:
                main_character.move_left = True
            if ev3nt.type == KEYUP and ev3nt.key == K_RIGHT:
                main_character.move_right = False

            if ev3nt.type == KEYDOWN and ev3nt.key == K_RIGHT:
                main_character.move_right = True
            if ev3nt.type == KEYUP and ev3nt.key == K_LEFT:
                main_character.move_left = False

        main_character.update(main_character.move_left, main_character.move_right, main_character.move_up, platforms)
        camera.update(main_character)
        for obj in objects:
            screen.blit(obj.image, camera.apply(obj))
        pygame.display.update()


if __name__ == "__main__":
    main()
