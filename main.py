import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 60
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(PLAYER_GREEN)
        self.rect = self.image.get_rect()
        self.movex = 0
        self.movey = 0

        self.health = 15
        self.is_colliding = False

    # Allows the player to move.
    def control(self, x, y):
        self.movex += x
        self.movey += y

    # Updates player position/stats each frame.
    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in enemy_hit_list:
            self.health -= 1
            print(self.health)

        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for ground in ground_hit_list:
            self.movey = 0
            self.rect.y = worldy - self.height - 30
            self.is_colliding = True

        platform_hit_list = pygame.sprite.spritecollide(
            self, platform_list, False)
        for platform in platform_hit_list:
            self.movey = 0
            self.is_colliding = True
            if self.rect.y > platform.rect.y:
                self.rect.y = platform.rect.y + platform.rect.height
            else:
                self.rect.y = platform.rect.y - self.height + 1

        quicksand_hit_list = pygame.sprite.spritecollide(
            self, quicksand_list, False)
        for quicksand in quicksand_hit_list:
            self.movey = 0
            self.is_colliding = True

    def gravity(self):
        if self.rect.y > worldy and self.movey > 0:
            self.movey = 0
            self.rect.y = worldy - self.height
        elif self.rect.y != worldy - self.height - 30:
            self.movey += 3

    def jump(self):
        if self.is_colliding == True:
            self.movey -= 33

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 60
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(ENEMY_RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
        self.is_colliding = True

    def move(self):
        distance = 80
        speed = 4

        if 0 <= self.counter <= distance:
            self.rect.x += speed
        elif distance <= self.counter <= distance * 2:
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1

        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for ground in ground_hit_list:
            self.movey = 0
            self.rect.y = ground.rect.y - self.height
            self.is_colliding = True

        platform_hit_list = pygame.sprite.spritecollide(
            self, platform_list, False)
        for platform in platform_hit_list:
            self.movey = 0
            self.is_colliding = True
            if self.rect.y > platform.rect.y:
                self.rect.y = platform.rect.y + platform.rect.height
            else:
                self.rect.y = platform.rect.y - self.height + 1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Level():
    @staticmethod
    def bad(lvl, enemy_location):
        if lvl == 1:
            enemy = Enemy(enemy_location[0], enemy_location[1])
            enemy_list = pygame.sprite.Group()
            enemy_list.add(enemy)
        if lvl == 2:
            enemy_list = None
            print(f"Level {lvl}")

        return enemy_list

    @staticmethod
    def ground(lvl, x, y, width, height):
        ground = Platform(x, y, width, height, PLATFORM_BLACK)

        ground_list = pygame.sprite.Group()
        if lvl == 1:
            ground = Platform(x, y, width, height, PLATFORM_BLACK)
            ground_list.add(ground)

        return ground_list


"""
Setup
"""
# Screen size
worldx = 800
worldy = 600

forwardx = 700
forwardy = 100
backwardx = 100
backwardy = 500

world = pygame.display.set_mode([worldx, worldy])

# Framerate
fps = 60

# Colors
BLUE = (70, 130, 250)
ENEMY_RED = (220, 100, 100)
PLAYER_GREEN = (100, 220, 100)
PLATFORM_BLACK = (10, 10, 10)
GROUND_WHITE = (245, 245, 245)
SAND_TAN = (252, 230, 174)

# Animation cycles
ani = 4
clock = pygame.time.Clock()

# Player position
player = Player()
player.rect.x = 150
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)

# Enemy position
enemy_location = [200, 20]
enemy_list = Level.bad(1, enemy_location)

# Platforms
platform1 = Platform(650, 385, 150, 125, PLATFORM_BLACK)
platform2 = Platform(200, 78, 300, 100, PLATFORM_BLACK)
platform3 = Platform(850, 250, 400, 50, PLATFORM_BLACK)

platform_list = [platform1, platform2, platform3]

quicksand1 = Platform(400, 300, 100, 200, SAND_TAN)

ground = Platform(0, 570, 800, 30, (GROUND_WHITE))

platform_list = pygame.sprite.Group()
platform_list.add(platform1)
platform_list.add(platform2)
platform_list.add(platform3)
quicksand_list = pygame.sprite.Group()
quicksand_list.add(quicksand1)
ground_list = pygame.sprite.Group()
ground_list.add(ground)

# big steppy
steps = 10

# START!
pygame.init
main = True
"""
Main Loop
"""
while main == True:
    world.fill(BLUE)
    player.update()
    player_list.draw(world)
    enemy_list.draw(world)
    platform_list.draw(world)
    quicksand_list.draw(world)
    ground_list.draw(world)
    for e in enemy_list:
        e.move()
    pygame.display.flip()
    clock.tick(fps)

    player.gravity()

    if player.rect.x >= forwardx:
        scroll = player.rect.x - forwardx
        player.rect.x = forwardx

        for platform in platform_list:
            platform.rect.x -= scroll

        for quicksand in quicksand_list:
            quicksand.rect.x -= scroll

        for enemy in enemy_list:
            enemy.rect.x -= scroll
    elif player.rect.x <= backwardx:
        scroll = backwardx - player.rect.x
        player.rect.x = backwardx

        for platform in platform_list:
            platform.rect.x += scroll

        for quicksand in quicksand_list:
            quicksand.rect.x += scroll

        for enemy in enemy_list:
            enemy.rect.x += scroll

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
            if event.key == pygame.K_UP or event.key == ord(
                    'w') or event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.height = 30

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.height = 60
            if event.key == ord('q'):
                pygame.quit()
                main = False
