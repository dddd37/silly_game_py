import pygame
import random
import sys
import os

# Инициализация Pygame
pygame.init()

# Константы для экрана
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 790
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Цветные пузыри")

# Путь к папке со спрайтами
SPRITES_PATH = os.path.join(os.path.dirname(__file__), 'sprites')

# Загрузка фона и облаков
background = pygame.image.load(os.path.join(SPRITES_PATH, 'sky.jpg')).convert()
background = pygame.transform.smoothscale(background, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
background = pygame.transform.smoothscale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
shield_image = pygame.image.load(os.path.join(SPRITES_PATH, 'shield.png')).convert_alpha()
timer_image = pygame.image.load(os.path.join(SPRITES_PATH, 'timer.png')).convert_alpha()

# Цвета
GREEN = (94, 205, 147)
PINK = (248, 102, 254)
YELLOW = (186, 237, 8)
BLUE = (93, 163, 253)
WHITE = (222, 210, 246)
DARK = (73, 50, 95)
SILVER = (192, 192, 192)
FREEZE = (102, 224, 255)
SHARP = (255,87,87)

# Класс для облаков
class Clouds(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, is_angry=False):
        super().__init__()
        self.image = None
        self.rect = None
        self.is_angry = is_angry
        self.load_cloud()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def load_cloud(self, size=(200, 100)):
        if self.is_angry:
            cloud_image = 'angry_cloud.png'
        else:
            cloud_images = ['cloud1.png', 'cloud2.png', 'cloud3.png', 'cloud4.png', 'cloud5.png', 'cloud6.png']
            cloud_image = random.choice(cloud_images)
        self.image = pygame.image.load(os.path.join(SPRITES_PATH, cloud_image)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.image.set_alpha(160)
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

    def update(self):
        if self.speed == 0:  # Если скорость облака равна 0, пропускаем обновление
            return
        
        self.rect.y += self.speed  # Движение облака вниз

        # Проверка, достигло ли облако нижней границы экрана
        if self.rect.top >= SCREEN_HEIGHT:
            self.rect.y = -self.rect.height-2
            self.rect.x = random.randint(2, SCREEN_WIDTH - 2)

        # Обновление скорости облака при заморозке времени
        if self.speed != 0.85:  # Проверяем, заморожено ли время
            if self.is_angry:  # Если облако злое
                self.speed = 0.51
            else:
                self.speed = 0.51 # Устанавливаем скорость облака




# Класс для шаров
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, color, zigzag=False): 
        super().__init__()
        radius = 15
        self.radius = radius
        image_size = (40, 40)

        # Бонусные шары
        if random.random() < 0.2:
            rand = random.random()
            if rand < 0.33:
                color = SILVER                
                self.image = pygame.Surface((46, 46), pygame.SRCALPHA)
                pygame.draw.circle(self.image, color, (23, 23), 23)
                pygame.draw.circle(self.image, color, (23, 23), 23, 3)
                image = pygame.image.load('./sprites/shield.png').convert_alpha()
                image = pygame.transform.smoothscale(image, image_size)
                image_rect = image.get_rect(center=(radius, radius))
                self.image.blit(image, image_rect.move(8, 9))
            elif rand < 0.66:
                color = FREEZE
                self.image = pygame.Surface((46, 46), pygame.SRCALPHA)
                pygame.draw.circle(self.image, color, (23, 23), 23)
                pygame.draw.circle(self.image, color, (23, 23), 23, 3)
                image = pygame.image.load('./sprites/timer.png').convert_alpha()
                image = pygame.transform.smoothscale(image, image_size)
                image_rect = image.get_rect(center=(radius, radius))
                self.image.blit(image, image_rect.move(8, 8))
            else:
                dart_size = (30, 30)
                color = SHARP
                self.image = pygame.image.load(os.path.join(SPRITES_PATH, 'dart.png')).convert_alpha()
                self.image = pygame.transform.scale(self.image, dart_size)
                self.image = pygame.transform.rotate(self.image, -45)
                self.mask = pygame.mask.from_surface(self.image)
        else: # Обычные шары
            self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, color, (radius, radius), radius)
            pygame.draw.circle(self.image, (0, 0, 0), (radius, radius), radius, 3)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.speed = random.uniform(2.6, 6.6)
        self.color = color
        self.zigzag = zigzag  # Движение зигзагом
        self.dx = random.choice([-1, 1])  # Направление по оси X
        self.dy = 1  # Направление по оси Y

    def update(self):
        if self.zigzag:
            self.rect.x += self.dx
            self.rect.y += self.speed * self.dy
            if self.rect.left <= 2 or self.rect.right >= SCREEN_WIDTH - 2:
                # Проверяем, находится ли шар вплотную к стене перед изменением направления
                if self.rect.left <= 2:
                    self.rect.left = 2  # Выравниваем шар по границе слева
                elif self.rect.right >= SCREEN_WIDTH - 2:
                    self.rect.right = SCREEN_WIDTH - 2  # Выравниваем шар по границе справа
                self.dx *= -1  # Меняем направление по оси X
        else:
            self.rect.y += self.speed
            if self.rect.left <= 2 or self.rect.right >= SCREEN_WIDTH - 2:
                # Проверяем, находится ли шар вплотную к стене перед изменением направления
                if self.rect.left <= 2:
                    self.rect.left = 2  # Выравниваем шар по границе слева
                elif self.rect.right >= SCREEN_WIDTH - 2:
                    self.rect.right = SCREEN_WIDTH - 2  # Выравниваем шар по границе справа
                self.dx *= -1  # Меняем направление по оси X
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()



# Класс для главного пузыря
class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        radius = 24
        self.radius = radius
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        pygame.draw.circle(self.image, (0, 0, 0), (radius, radius), radius, 4)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
        self.color = color
        self.speed = 5  
        self.shield_duration = 0
        self.shield_active = False  # Флаг, указывающий, активен ли щит
        self.freeze_duration = 0  # добавляем переменную для отслеживания времени замедления
        self.freeze_active = False  # Флаг, указывающий, активно ли замедление
        self.shock_duration = 0 # продолжительность действия грозового облака
        self.shock_active = False # Флаг встречи с грозовым облаком


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 3:  
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH - 3:  
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 3:  
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:  
            self.rect.y += self.speed




# Главная функция
class MainGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 800))
        pygame.display.set_caption("Цветные пузыри")
        self.clock = pygame.time.Clock()
        self.time_passed = 0
        self.angry_cloud_probability=0.099

        # Загрузка фона и облаков
        self.background = pygame.image.load(os.path.join(SPRITES_PATH, 'sky.jpg')).convert()
        self.background = pygame.transform.smoothscale(self.background, (250, 400))
        self.background = pygame.transform.smoothscale(self.background, (500, 800))

        self.score = 0  # Инициализация счетчика очков
        self.paused = False  # Переменная для отслеживания состояния паузы

        # Создание групп спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.clouds_group = pygame.sprite.Group()  # Группа для облаков

        # Создание нескольких облаков
        self.create_clouds()
        
        # Создание игрока
        color_for_player = random.choice([PINK, YELLOW, GREEN, WHITE, BLUE])
        self.player = Player(color_for_player)
        self.all_sprites.add(self.player)

        # Настройка частоты появления шаров
        self.frame_count = 0
        self.frame_rate = 40

    def toggle_pause(self):
        self.paused = not self.paused

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.toggle_pause()

            if not self.paused:  # Проверяем, не находится ли игра в режиме паузы
                self.frame_count += 1
                if self.frame_count % self.frame_rate == 0:
                    color = random.choice([PINK, YELLOW, GREEN, WHITE, BLUE])
                    zigzag = random.random() < 0.33
                    ball = Ball(random.uniform(14.5, SCREEN_WIDTH-14.5), 0, color, zigzag)
                    self.all_sprites.add(ball)
                    self.balls.add(ball)
                

                # Обновление позиций спрайтов
                self.all_sprites.update()
                self.clouds_group.update()

                # Проверка на столкновение шаров с главным пузырем
                hits = pygame.sprite.spritecollide(self.player, self.balls, True, pygame.sprite.collide_mask)
                if hits:
                    for hit in hits:
                        if hit.color != self.player.color:
                            if hit.color == SILVER:
                                self.player.shield_duration = 5.2  # Устанавливаем время невосприимчивости
                                self.player.shield_active = True
                            elif hit.color == FREEZE:
                                self.player.freeze_duration = 5.2  # устанавливаем время замедления
                                self.player.freeze_active = True
                                self.time_freezer()
                            elif hit.color == SHARP and self.player.shield_active==False:
                                self.score -= 2  # устанавливаем урон
                                if self.score < 0:
                                    self.game_over()
                            else:
                                if self.player.shield_duration <= 0:
                                    self.game_over()
                                else:
                                    if hit.color != self.player.color:
                                        self.score += 1
                        else:
                            self.score += 1

                angry_cloud_hits = pygame.sprite.spritecollide(self.player, self.clouds_group, False, pygame.sprite.collide_mask)
                if angry_cloud_hits:
                    for cloud in angry_cloud_hits:
                        if cloud.is_angry and self.player.shield_active==False:
                            self.player.shock_duration = 2.2
                            self.player.shock_active=True
                            self.player.speed=0

                 # Обновление таймера действия щита, времени замедления, грозы
                if self.player.shield_active:
                    self.player.shield_duration -= self.clock.get_time() / 1000
                    if self.player.shield_duration <= 0:
                        self.player.shield_active = False
                
                if self.player.freeze_active:
                    self.player.freeze_duration -= self.clock.get_time() / 1000
                    if self.player.freeze_duration <= 0:
                        self.player.freeze_active = False
                        self.time_freezer()

                if self.player.shock_active:
                    self.player.shock_duration -= self.clock.get_time() / 1000
                    if self.player.shock_duration <= 0:
                        self.player.shock_active = False
                        self.player.speed=5
                        
                # Проверка расстояния между нижним краем экрана и самым нижним облаком в группе
                if not self.clouds_group or SCREEN_HEIGHT - self.clouds_group.sprites()[-1].rect.bottom < 400:
                    self.create_clouds()


                self.time_passed += self.clock.get_time() / 1000

   
            # Отображение фона
            self.screen.blit(self.background, (0, 0))

            # Отображение облаков
            self.clouds_group.draw(self.screen)

            # Отображение спрайтов
            self.all_sprites.draw(self.screen)

            # Отображение счетчика очков
            self.draw_text(f'Score: {self.score}', 30, WHITE, 10, 10)

            # Отображение времени
            self.draw_text(f'Time: {int(self.time_passed)}', 30, WHITE, SCREEN_WIDTH - 120, 10)

            # Отображение текста "Paused" при паузе
            if self.paused:
                self.draw_text("Paused", 40, WHITE, 200, 10)

            # Отображение таймера действия щита 
            if self.player.shield_active:
                remaining_time = max(0, int(self.player.shield_duration))  # Округляем значение до целого числа
                self.draw_text(f'Shield: {remaining_time}s', 30, WHITE, SCREEN_WIDTH - 110, 750)

            # Отображение таймера действия замедления времени 
            if self.player.freeze_active:
                remaining_time = max(0, int(self.player.freeze_duration))  # Округляем значение до целого числа
                self.draw_text(f'Freeze: {remaining_time}s', 30, WHITE, SCREEN_WIDTH - 110, 770)

            # Отображение таймера действия грозы 
            if self.player.shock_active:
                remaining_time = max(0, int(self.player.shock_duration))  # Округляем значение до целого числа
                self.draw_text(f'Storm: {remaining_time}s', 30, WHITE, SCREEN_WIDTH - 110, 730)


            # Обновление экрана
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

        pygame.quit()
        sys.exit()

    def game_over(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()  # Начинаем игру заново
                        self.run()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            self.draw_text("You lost!", 75, (255, 112, 112), 140, 375)

            pygame.display.flip()
            self.clock.tick(30)


    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_outline_surface = font.render(text, True, DARK)
        text_rect = text_surface.get_rect(topleft=(x, y))
        text_outline_rect = text_outline_surface.get_rect(topleft=(x, y))
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                text_outline_rect.topleft = (x + dx, y + dy)
                self.screen.blit(text_outline_surface, text_outline_rect)
        self.screen.blit(text_surface, text_rect)

    def time_freezer(self):
        for ball in self.balls:
            ball.speed = random.uniform(1.6, 2.6) if self.player.freeze_active else random.uniform(5.6, 6.6)
        for cloud in self.clouds_group:  
            cloud.speed = 0.51 if self.player.freeze_active else 0.85
        self.player.speed = 2.5 if self.player.freeze_active else 5
        self.clouds_group.update()



    def create_clouds(self):
        for _ in range(random.randint(1, 3)):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-100, -50)  
            if random.random() < self.angry_cloud_probability:
                cloud = Clouds(x, y,speed=0.85,  is_angry=True)
                self.clouds_group.add(cloud)
            else:
                cloud = Clouds(x, y,speed=0.85, is_angry=False)
                self.clouds_group.add(cloud)
    

if __name__ == "__main__":
    game = MainGame()
    game.run()