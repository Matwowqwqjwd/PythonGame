import pygame
import random

# Inicializar PyGame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Cargar imágenes
ship_img = pygame.image.load("imagenes/ship.png")
asteroid_img = pygame.image.load("imagenes/asteroid.png")
bullet_img = pygame.image.load("imagenes/bullet.png")

# Clases del juego
class Ship:
    def __init__(self):
        self.image = pygame.transform.scale(ship_img, (50, 50))
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.speed = 5
        self.alive = True
    
    def move(self, dx):
        self.x = max(0, min(WIDTH - 50, self.x + dx))
    
    def draw(self):
        if self.alive:
            screen.blit(self.image, (self.x, self.y))

    def check_collision(self, asteroids):
        for asteroid in asteroids:
            if pygame.Rect(self.x, self.y, 50, 50).colliderect(pygame.Rect(asteroid.x, asteroid.y, 40, 40)):
                self.alive = False

class Bullet:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.x = x + 20
        self.y = y
        self.speed = 7
    
    def move(self):
        self.y -= self.speed
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Asteroid:
    def __init__(self):
        self.image = pygame.transform.scale(asteroid_img, (40, 40))
        self.x = random.randint(0, WIDTH - 40)
        self.y = -40
        self.speed = random.randint(2, 5)
    
    def move(self):
        self.y += self.speed
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

def game_loop():
    clock = pygame.time.Clock()
    ship = Ship()
    bullets = []
    asteroids = []
    running = True
    score = 0
    
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship.move(-ship.speed)
        if keys[pygame.K_RIGHT]:
            ship.move(ship.speed)
        if keys[pygame.K_SPACE]:
            bullets.append(Bullet(ship.x, ship.y))
        
        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < 0:
                bullets.remove(bullet)
        
        if random.randint(1, 50) == 1:
            asteroids.append(Asteroid())
        
        for asteroid in asteroids[:]:
            asteroid.move()
            if asteroid.y > HEIGHT:
                asteroids.remove(asteroid)
        
        # Detección de colisiones entre balas y asteroides
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if pygame.Rect(bullet.x, bullet.y, 10, 20).colliderect(pygame.Rect(asteroid.x, asteroid.y, 40, 40)):
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 1
                    break
        
        ship.check_collision(asteroids)
        if not ship.alive:
            running = False
        
        ship.draw()
        for bullet in bullets:
            bullet.draw()
        for asteroid in asteroids:
            asteroid.draw()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

game_loop()
