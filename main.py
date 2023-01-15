import pygame

# Initialiser Pygame
pygame.init()

# Initialize the mixer module
pygame.mixer.init()
# Load the sound effect
laser_sound = pygame.mixer.Sound("laser.wav")

# Définir la taille de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Créer la fenêtre de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Charger l'image d'arrière-plan
bg_image = pygame.image.load("background.png")

explosion_animation = []
for i in range(9):
    filename = f"explosion0{i}.png"
    image = pygame.image.load(filename).convert()
    image.set_colorkey((0, 0, 0))  # noir
    explosion_animation.append(image)

# Classe de l'explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_animation[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Charger l'image de l'ennemi et rendre le fond transparent
        self.x = x
        self.y = y
        self.image = pygame.image.load("enemy.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1

    def update(self):
        self.y += self.speed
        self.rect.center = (self.x, self.y)

# Classe du laser
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0))  # rouge
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10  # vitesse de déplacement vers le haut
    def update(self):
        self.rect.y += self.speedy
    def collide(self, enemy):
            return self.rect.colliderect(enemy.rect)

# Classe du sprite
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Charger l'image de l'alien et rendre le fond transparent
        self.image = pygame.image.load("alien.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5  # vitesse de déplacement

    def update(self):
        # Récupérer l'état des touches
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
    def fire(self):
        laser = Laser(self.rect.centerx, self.rect.top)
        all_sprites.add(laser)
        lasers.add(laser)
         # Play the sound effect
        laser_sound.play()


# Créer le sprite
alien = Alien()
all_sprites = pygame.sprite.Group()
all_sprites.add(alien)

lasers = pygame.sprite.Group()

# Créer un groupe de sprites pour les explosions
explosion_group = pygame.sprite.Group()

# Créer les ennemis
enemies = pygame.sprite.Group()
for i in range(4):
    enemy = Enemy(SCREEN_WIDTH * (0.2 + i * 0.2), SCREEN_HEIGHT * 0.1)
    enemies.add(enemy)
    all_sprites.add(enemy)

# Fonction de détection de collision
def collide(obj1, obj2):
    if obj1.rect.colliderect(obj2.rect):
        return True
    else:
        return False

# Boucle principale du jeu
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupérer l'état des touches
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        alien.fire()

    # Détecter les collisions entre les lasers et les ennemis
    for laser in lasers:
        for enemy in enemies:
            if collide(laser, enemy):
                # Créer une explosion à l'emplacement de l'ennemi
                explosion = Explosion(enemy.rect.center)
                explosion_group.add(explosion)
                all_sprites.add(explosion)
                # Supprimer l'ennemi et le laser
                enemies.remove(enemy)
                all_sprites.remove(enemy)
                lasers.remove(laser)
    
    # Mettre à jour le sprite
    all_sprites.update()
    
    # Dessiner l'arrière-plan
    screen.blit(bg_image, (0, 0))
    
    # Dessiner le sprite
    all_sprites.draw(screen)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
