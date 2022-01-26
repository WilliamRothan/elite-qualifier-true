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

    platform_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
    for platform in platform_hit_list:
      self.movey = 0
      self.is_colliding = True
      if self.rect.y > platform.rect.y:
        self.rect.y = platform.rect.y + platform.rect.height
      else:
        self.rect.y = platform.rect.y - self.height + 1

    quicksand_hit_list = pygame.sprite.spritecollide(self, quicksand_list, False)
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
    self.is_colliding = False

  def move(self):
    distance = 80
    speed = 4

    if 0 <= self.counter <= distance:
      self.rect.x += speed
    elif distance <= self.counter <= distance * 2:
      self.rect.x -= speed
    else:
      self.counter = 0
    
    if self.is_colliding == False:
      self.rect.y += 3

    self.counter += 1

    ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
    for ground in ground_hit_list:
      self.movey = 0
      self.rect.y = ground.rect.y - self.height
      self.is_colliding = True

    platform_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
    for platform in platform_hit_list:
      self.movey = 0
      self.is_colliding = True
      if self.rect.y > platform.rect.y:
        self.rect.y = platform.rect.y + platform.rect.height
      else:
        self.rect.y = platform.rect.y - self.height + 1
  def gravity(self):
    if self.rect.y > worldy and self.movey > 0:
      self.movey = 0
      self.rect.y = worldy - self.height
    elif self.rect.y != worldy - self.height - 30:
      self.movey += 3


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
lvl = 1

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
player.rect.y = 570
player_list = pygame.sprite.Group()
player_list.add(player)

ground = Platform(0, 570, 800, 30, GROUND_WHITE)

# Level 1
platform1_1 = Platform(650, 385, 150, 125, PLATFORM_BLACK)
platform1_2 = Platform(200, 78, 300, 100, PLATFORM_BLACK)
platform1_3 = Platform(850, 250, 400, 50, PLATFORM_BLACK)
quicksand1_1 = Platform(400, 300, 100, 200, SAND_TAN)
platform_list = [platform1_1, platform1_2, platform1_3]

enemy1_1 = Enemy(200, 20)
enemy1_2 = Enemy(400, 510)
enemy_list = [enemy1_1, enemy1_2]

# Level 2
quicksand2_1 = Platform(650, 385, 150, 125, SAND_TAN)
quicksand2_2 = Platform(1000, 450, 250, 120, SAND_TAN)
quicksand2_3 = Platform(300, 200, 450, 120, SAND_TAN)

platform_list = pygame.sprite.Group()
platform_list.add(platform1_1)
platform_list.add(platform1_2)
platform_list.add(platform1_3)
quicksand_list = pygame.sprite.Group()
quicksand_list.add(quicksand1_1)
ground_list = pygame.sprite.Group()
ground_list.add(ground)

enemy_list = pygame.sprite.Group()
enemy_list.add(enemy1_1)
enemy_list.add(enemy1_2)

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
      if event.key == pygame.K_UP or event.key == ord('w') or event.key == pygame.K_SPACE:
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
      if event.key == ord('l') and lvl <= 2:
        lvl += 1
        player.rect.x = 150
        player.rect.y = 570
      if event.key == ord('q'):
          pygame.quit()
          main = False
  
  if lvl == 1:
    platform_list.add(platform1_1)
    platform_list.add(platform1_2)
    platform_list.add(platform1_3)
    quicksand_list.add(quicksand1_1)
    enemy_list.add(enemy1_1)
    enemy_list.add(enemy1_2)
  
  if lvl ==2:
    platform_list.remove(platform1_1)
    platform_list.remove(platform1_2)
    platform_list.remove(platform1_3)
    quicksand_list.remove(quicksand1_1)
    enemy_list.remove(enemy1_1)
    enemy_list.remove(enemy1_2)

    quicksand_list.add(quicksand2_1)
    quicksand_list.add(quicksand2_2)
    quicksand_list.add(quicksand2_3)

# Bugs
# - Infinite jump
# - Platform collision only snaps to top or bottom (no wall cling/wall jump)
# - Crouch only shifts the sprite, it does not resize it
# - Enemy is not affected by gravity for some reason. Also unaffected by level switching.
# - Player has no i-frames when hit by an enemy, so their health gets melted really quickly.

# Things to add
# - HUD for player stats, points, whatever else.
# - Custom sprites
# - Larger levels
# - More than just 2 levels
# - Proper level start/end triggers. Currently, the level switch is bound to "L".
# - Invisible wall at the start of the level.
# - Different enemy types, as well as repositioning enemies in between levels
# - Invulnerability period after the player gets hit, in which their sprite (until a proper sprite is made) will change color. This will eventually be replaced by a stagger sprite.
# - Ways to attack/remove the enemies
# - Other platform types (potentially things like lava, ice, etc.)