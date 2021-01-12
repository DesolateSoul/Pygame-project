from pygame import *
import pygame
import pyganim
import random
import datetime

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
DISPLAY = (WINDOW_WIDTH, WINDOW_HEIGHT)
BACKGROUND_COLOR = "#000000"
FPS = 60
# Постоянные для игрока
MOVE_SPEED = 14
WIDTH = 52  # Размеры
HEIGHT = 64
COLOR = "#000000"
JUMP_POWER = 20
GRAVITY = 0.7
# Постоянные для платформ
PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 64
PLATFORM_LENGTH = 7
# Анимации
ANIMATION_RUN = [('data/run1.png', 0.1), ('data/run2.png', 0.1), ('data/run3.png', 0.1), ('data/run4.png', 0.1),
                 ('data/run5.png', 0.1), ('data/run6.png', 0.1)]
ANIMATION_JUMP = [('data/jump1.png', 0.2), ('data/jump2.png', 0.2), ('data/jump3.png', 0.2),
                  ('data/jump4.png', 0.2), ('data/jump5.png', 0.2), ('data/jump6.png', 0.2)]
ANIMATION_STAY = [('data/idle1.png', 0.2), ('data/idle2.png', 0.2), ('data/idle3.png', 0.2),
                  ('data/idle4.png', 0.2)]
ANIMATION_ATTACK1 = [('data/attack_1_1.png', 0.1), ('data/attack_1_2.png', 0.1), ('data/attack_1_3.png', 0.1),
                     ('data/attack_1_4.png', 0.1), ('data/attack_1_5.png', 0.1), ('data/attack_1_6.png', 0.1)]
ANIMATION_ATTACK1_LEFT = [('data/attack_1_1_left.png', 0.1), ('data/attack_1_2_left.png', 0.1),
                          ('data/attack_1_3_left.png', 0.1), ('data/attack_1_4_left.png', 0.1),
                          ('data/attack_1_5_left.png', 0.1), ('data/attack_1_6_left.png', 0.1)]
pygame.init()
# Звуки
PLATFORM_SOUND1 = pygame.mixer.Sound('data/wood1.mp3')
PLATFORM_SOUND2 = pygame.mixer.Sound('data/wood2.mp3')
PLATFORM_SOUND3 = pygame.mixer.Sound('data/wood3.mp3')
PLATFORM_SOUND4 = pygame.mixer.Sound('data/wood4.mp3')
PLATFORM_SOUND5 = pygame.mixer.Sound('data/stone.mp3')
PLATFORM_SOUND5.set_volume(0.1)
FALL_SOUND = pygame.mixer.Sound('data/fall.mp3')
BIG_FALL_SOUND = pygame.mixer.Sound('data/fall_big.mp3')
WIN_SOUNDS = pygame.mixer.Sound('data/win_sounds.mp3')
ANIMATION_TIME = datetime.timedelta(milliseconds=600)
FONT = pygame.font.Font(None, 50)

SCREEN = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Платформер")
BACKGROUND = image.load("data/background.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (4096, 2048))
MENU_IMAGE = image.load("data/menu_image.jpg")
MENU_IMAGE = pygame.transform.scale(MENU_IMAGE, DISPLAY)
TIMER = pygame.time.Clock()


class Player(sprite.Sprite):
    def __init__(self, x, y, move_left=False, move_right=False, move_up=False, attack=False, gaze_direction="right",
                 blocks_in_inventory=0, fall_sounds=0, walk_sound_count=1):
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
        self.blocks_in_inventory = blocks_in_inventory
        self.fall_sounds = fall_sounds
        self.walk_sound_count = walk_sound_count

        self.attack = attack
        self.gaze_direction = gaze_direction  # Направление взгляда
        self.image = Surface((76, 76))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        #  Анимация движения вправо
        self.animation_run = pyganim.PygAnimation(ANIMATION_RUN)
        self.animation_run.play()
        #  Анимация бездействия
        self.animation_stay = pyganim.PygAnimation(ANIMATION_STAY)
        self.animation_stay.play()
        #  Анимация прыжка вправо
        self.animation_jump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.animation_jump.play()

        self.animation_attack1 = pyganim.PygAnimation(ANIMATION_ATTACK1)
        self.animation_attack1.play()

        self.animation_attack1_left = pyganim.PygAnimation(ANIMATION_ATTACK1_LEFT)
        self.animation_attack1_left.play()

        self.animation_run.scale((WIDTH, HEIGHT))
        self.animation_stay.scale((WIDTH, HEIGHT))
        self.animation_jump.scale((WIDTH, HEIGHT))
        self.animation_attack1.scale((self.animation_attack1.getRect()[2] * 2, self.animation_attack1.getRect()[3] * 2))
        self.animation_attack1_left.scale((self.animation_attack1_left.getRect()[2] * 2,
                                           self.animation_attack1_left.getRect()[3] * 2))
        self.animation_stay.blit(self.image, (0, 0))  # По-умолчанию, стоим

    def update(self, left, right, up, attack, platforms, time_was=datetime.datetime.now()):
        if up:
            if self.ground_touch:  # Прыгаем, только когда можем оттолкнуться от земли
                self.y_speed = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.animation_jump.blit(self.image, (0, 0))
        if left:
            self.x_speed = -MOVE_SPEED
            self.image.fill(Color(COLOR))
            if up:
                self.animation_jump.blit(self.image, (0, 0))
            else:
                self.animation_run.blit(self.image, (0, 0))
        if right:
            self.x_speed = MOVE_SPEED
            self.image.fill(Color(COLOR))
            if up:
                self.animation_jump.blit(self.image, (0, 0))
            else:
                self.animation_run.blit(self.image, (0, 0))
        if not (left or right):  # Стоим, когда нет указаний идти
            self.x_speed = 0
            if attack:
                if self.gaze_direction == "right":
                    self.image.fill(Color(COLOR))
                    self.animation_attack1.blit(self.image, (0, 0))
                elif self.gaze_direction == "left":
                    self.image.fill(Color(COLOR))
                    self.animation_attack1_left.blit(self.image, (0, 0))
            elif not up and self.ground_touch:
                self.image.fill(Color(COLOR))
                self.animation_stay.blit(self.image, (0, 0))
        if not self.ground_touch:  # изменение скорости в зависимости от гравитации
            self.y_speed += GRAVITY

        self.ground_touch = False
        self.rect.y += self.y_speed  # Изменение положения квадрата игрока
        self.collide(0, self.y_speed, platforms, time_was)  # Проверка столкновений
        self.rect.x += self.x_speed  # Изменение положения квадрата игрока
        self.collide(self.x_speed, 0, platforms, time_was, self.attack)  # Проверка столкновений

    def can_attack(self, platform):
        if self.rect.x + WIDTH == platform.rect.x and self.rect.y == platform.rect.y \
                and self.gaze_direction == "right" and not self.move_right:
            return True
        elif self.rect.x == platform.rect.x + PLATFORM_WIDTH and self.rect.y == platform.rect.y \
                and self.gaze_direction == "left" and not self.move_left:
            return True
        else:
            return False

    def collide(self, x_speed, y_speed, platforms, time_was, attack=False):
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
                    if self.fall_sounds == 1:
                        FALL_SOUND.play()
                        self.fall_sounds -= 1
                    elif self.fall_sounds == 2:
                        BIG_FALL_SOUND.play()
                        self.fall_sounds -= 2
                if y_speed < 0:
                    self.rect.top = platform.rect.bottom
                    self.y_speed = 0
            if self.can_attack(platform) and attack:
                platform.update_condition(platforms, time_was, self)

    def place_platform(self, platforms, objects):
        if self.blocks_in_inventory >= 1:
            if self.gaze_direction == 'right':
                placed_platform = Platform(self.rect.x + WIDTH, self.rect.y)
            else:
                placed_platform = Platform(self.rect.x - PLATFORM_WIDTH, self.rect.y)
            if not sprite.spritecollide(placed_platform, objects, dokill=False):
                platforms.append(placed_platform)
                objects.add(placed_platform)
                self.blocks_in_inventory -= 1
        return platforms, objects


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

    g = min(0, g)  # Не движемся дальше левой границы
    g = max(-(camera.width - WINDOW_WIDTH), g)  # Не движемся дальше правой границы
    t = max(-(camera.height - WINDOW_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы
    return Rect(g, t, w, h)


def generate_level(filename):
    with open(f"data/{filename}", mode="w", encoding="utf-8") as generated_level:
        for i in range(32):  # Генерация "коробки"
            for k in range(64):
                if i == 0 or i == 31:
                    print("*", end="", file=generated_level)
                    if k == 63:
                        print("", file=generated_level)
                elif k == 0:
                    print("*", end="", file=generated_level)
                elif k == 63:
                    print("*", file=generated_level)
                else:
                    print("", end=" ", file=generated_level)
    with open(f"data/{filename}", mode="r", encoding="utf-8") as generated_level:
        level = generated_level.read().splitlines()
        for i in range(len(level[1:-1])):  # Генерация платформ
            n = random.randint(1, len(level[0][1:-1]) - PLATFORM_LENGTH)
            for k in range(PLATFORM_LENGTH):
                level[i + 1] = level[i + 1][:n + k] + "-" + level[i + 1][n + k + 1:]
            level[3] = level[3][:61] + "**" + level[3][63:]
            level[2] = level[2][:63] + "-"
    return level


class Platform(sprite.Sprite):
    def __init__(self, x, y, condition=1, breakable=True):
        sprite.Sprite.__init__(self)
        self.breakable = breakable
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        if self.breakable:
            self.image = image.load("data/platform.png")
        else:
            self.image = image.load("data/platform_stone.png")
        self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.condition = condition
        self.time_was = datetime.datetime.now()

    def update_condition(self, platforms, time_was, main_hero):
        if datetime.datetime.now() - self.time_was >= ANIMATION_TIME:
            if self.breakable:
                if self.condition == 1:
                    self.time_was = time_was
                self.condition += 1
                if self.condition == 2:
                    self.time_was = datetime.datetime.now()
                if self.condition == 3:
                    self.image = image.load("data/platform_broken.png")
                    self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_WIDTH))
                    self.time_was = datetime.datetime.now()
                    exec(f'PLATFORM_SOUND{random.randint(1, 3)}.play()')  # Случайный звук при рубке
                elif self.condition == 4:
                    self.kill()
                    del platforms[platforms.index(self)]
                    PLATFORM_SOUND4.play()
                    if main_hero.blocks_in_inventory < 10:
                        main_hero.blocks_in_inventory += 1
            else:
                if self.condition == 1:
                    self.time_was = time_was
                self.condition += 1
                if self.condition == 2:
                    self.time_was = datetime.datetime.now()
                if self.condition >= 3:
                    self.time_was = datetime.datetime.now()
                    PLATFORM_SOUND5.play()


def main(in_menu=True, running=True, win=False):
    main_character = Player(64, 1920)
    objects = pygame.sprite.Group()  # Все объекты
    objects.add(main_character)
    platforms = []

    level = generate_level("level.txt")
    x = y = 0  # координаты установки платформ
    for line in level:
        for symbol in line:
            if symbol == "-":  # Деревянная платформа
                platform = Platform(x, y)
                objects.add(platform)
                platforms.append(platform)
            elif symbol == "*":  # Каменная платформа
                platform = Platform(x, y, breakable=False)
                objects.add(platform)
                platforms.append(platform)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Получившаяся длина уровня,
    total_level_height = len(level) * PLATFORM_HEIGHT  # высота
    camera = Camera(camera_configure, total_level_width, total_level_height)

    text1 = FONT.render("Приветствую в моей первой игре!", True, (255, 255, 255))
    text1_x = WINDOW_WIDTH // 2 - text1.get_width() // 2
    text1_y = 0

    text2 = FONT.render("Нажмите Enter чтобы начать игру", True, (255, 255, 255))
    text2_x = WINDOW_WIDTH // 2 - text1.get_width() // 2
    text2_y = WINDOW_HEIGHT - text2.get_height()

    text3 = FONT.render('Управление:', True, (255, 255, 255))
    text3_x = WINDOW_WIDTH // 2 - text3.get_width() // 2
    text3_y = WINDOW_HEIGHT // 4 - text3.get_height() // 4

    text4 = FONT.render('Стрелочки - передвижение', True, (255, 255, 255))
    text4_x = WINDOW_WIDTH // 2 - text4.get_width() // 2
    text4_y = WINDOW_HEIGHT // 4 - text4.get_height() // 4 + text3.get_height()

    text5 = FONT.render('Z - Атака, X - поставить платформу', True, (255, 255, 255))
    text5_x = WINDOW_WIDTH // 2 - text5.get_width() // 2
    text5_y = WINDOW_HEIGHT // 4 - text5.get_height() // 4 + text3.get_height() + text4.get_height()

    text6 = FONT.render('R - начать заново', True, (255, 255, 255))
    text6_x = WINDOW_WIDTH // 2 - text6.get_width() // 2
    text6_y = WINDOW_HEIGHT // 4 - text6.get_height() // 4 + \
        text3.get_height() + text4.get_height() + text5.get_height()

    text7 = FONT.render('Найдите выход чтобы победить!', True, (255, 255, 255))
    text7_x = WINDOW_WIDTH // 2 - text7.get_width() // 2
    text7_y = WINDOW_HEIGHT // 4 * 3 - text7.get_height() // 4 * 3

    while in_menu:  # Цикл меню
        SCREEN.blit(MENU_IMAGE, (0, 0))
        SCREEN.blit(text1, (text1_x, text1_y))
        SCREEN.blit(text2, (text2_x, text2_y))
        SCREEN.blit(text3, (text3_x, text3_y))
        SCREEN.blit(text4, (text4_x, text4_y))
        SCREEN.blit(text5, (text5_x, text5_y))
        SCREEN.blit(text6, (text6_x, text6_y))
        SCREEN.blit(text7, (text7_x, text7_y))
        for ev3nt in pygame.event.get():
            if ev3nt.type == QUIT:
                running = False
                in_menu = False
            if ev3nt.type == KEYUP and ev3nt.key == 13:
                in_menu = False
        pygame.display.flip()
    # Рисунок платформы рядом со счётчиком платформ в инвенторе
    wood_icon = pygame.image.load('data/platform.png')
    wood_icon = pygame.transform.scale(wood_icon, (PLATFORM_WIDTH // 2, PLATFORM_HEIGHT // 2))

    while running:  # Основной игровой цикл
        TIMER.tick(FPS)
        SCREEN.blit(BACKGROUND, (camera_configure(camera.state, main_character.rect).x,
                                 camera_configure(camera.state, main_character.rect).y))  # Перерисовка фона
        gaze_before = main_character.gaze_direction  # Направление взгляда игрока до событий
        if main_character.blocks_in_inventory == 10:
            blocks_in_inventory = FONT.render(str(main_character.blocks_in_inventory), True, (255, 0, 0))
        else:
            blocks_in_inventory = FONT.render(str(main_character.blocks_in_inventory), True, (255, 255, 255))

        for ev3nt in pygame.event.get():
            if ev3nt.type == QUIT:
                running = False
            if ev3nt.type == KEYDOWN and ev3nt.key == K_UP:
                main_character.move_up = True
            if ev3nt.type == KEYUP and ev3nt.key == K_UP:
                main_character.move_up = False

            if ev3nt.type == KEYDOWN and ev3nt.key == K_LEFT:
                main_character.move_left = True
                main_character.gaze_direction = "left"
            if ev3nt.type == KEYUP and ev3nt.key == K_LEFT:
                main_character.move_left = False

            if ev3nt.type == KEYDOWN and ev3nt.key == K_RIGHT:
                main_character.move_right = True
                main_character.gaze_direction = "right"
            if ev3nt.type == KEYUP and ev3nt.key == K_RIGHT:
                main_character.move_right = False

            if ev3nt.type == KEYDOWN and ev3nt.key == 122:  # Кнопка Z - атака
                main_character.attack = True
            if ev3nt.type == KEYUP and ev3nt.key == 122:
                main_character.attack = False

            if ev3nt.type == KEYDOWN and ev3nt.key == 120:  # Кнопка X - поставить платформу
                platforms, objects = main_character.place_platform(platforms, objects)

            if ev3nt.type == KEYDOWN and ev3nt.key == 114:  # Кнопка R - рестарт
                return main(False)
        # Условие победы
        if main_character.rect.x >= BACKGROUND.get_width():
            win = True
            running = False
            WIN_SOUNDS.play()
        # Проверка на то, проигрывать ли звук падения
        if main_character.fall_sounds == 0 and main_character.y_speed >= 18:
            main_character.fall_sounds += 1
        elif main_character.fall_sounds == 1 and main_character.y_speed >= 36:
            main_character.fall_sounds += 1
        # Взгляд после событий
        gaze_after = main_character.gaze_direction
        if gaze_before != gaze_after:  # Поворот анимаций при смене направления взгляда
            main_character.animation_run.flip(True, False)
            main_character.animation_stay.flip(True, False)
            main_character.animation_jump.flip(True, False)
        main_character.update(main_character.move_left, main_character.move_right, main_character.move_up,
                              main_character.attack, platforms)
        camera.update(main_character)
        for obj in objects:
            SCREEN.blit(obj.image, camera.apply(obj))
        # Отображение счётчика блоков в инвентаре
        SCREEN.blit(blocks_in_inventory, (10, 10))
        SCREEN.blit(wood_icon, (50, 10))

        pygame.display.update()

    text8 = FONT.render("Вы победили!", True, (255, 255, 255))
    text8_x = WINDOW_WIDTH // 2 - text8.get_width() // 2
    text8_y = WINDOW_HEIGHT // 2 - text8.get_height() // 2

    text9 = FONT.render("R - начать заново", True, (255, 255, 255))
    text9_x = WINDOW_WIDTH // 2 - text9.get_width() // 2
    text9_y = WINDOW_HEIGHT - text9.get_height()

    while win:  # Цикл победной картинки
        SCREEN.blit(MENU_IMAGE, (0, 0))
        SCREEN.blit(text8, (text8_x, text8_y))
        SCREEN.blit(text9, (text9_x, text9_y))
        for ev3nt in pygame.event.get():
            if ev3nt.type == QUIT:
                win = False
            if ev3nt.type == KEYUP and ev3nt.key == 13:
                win = False
            if ev3nt.type == KEYDOWN and ev3nt.key == 114:
                return main(False)
        pygame.display.flip()


if __name__ == "__main__":
    main()
