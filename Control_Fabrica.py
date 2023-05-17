import pygame
from pygame.locals import *
import os
import sys

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 586
IMG_DIR = "imagenes"
BG_COLOR = (100, 100, 100)
BUTTON_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)

def load_image(nombre, dir_imagen, width=None, height=None, alpha=False):
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    if width is not None and height is not None:
        image = pygame.transform.scale(image, (width, height))
    elif width is not None:
        aspect_ratio = float(image.get_height()) / float(image.get_width())
        image = pygame.transform.scale(image, (width, int(width * aspect_ratio)))
    elif height is not None:
        aspect_ratio = float(image.get_width()) / float(image.get_height())
        image = pygame.transform.scale(image, (int(height * aspect_ratio), height))
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

class Objeto(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = load_image(image_path, IMG_DIR)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


class CintaTransportadora(Objeto):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)

    def update(self):
        pass


class Robot(Objeto):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)
        self.target = None

    def update(self):
        if self.target:
            if self.rect.x < self.target.rect.x:
                self.rect.x += 1
            elif self.rect.x > self.target.rect.x:
                self.rect.x -= 1
            if self.rect.y < self.target.rect.y:
                self.rect.y += 1
            elif self.rect.y > self.target.rect.y:
                self.rect.y -= 1


class Contenedor(Objeto):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)

    def update(self):
        pass


def draw_button(screen, x, y, width, height, text, action):
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

    mouse_pos = pygame.mouse.get_pos()
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        if pygame.mouse.get_pressed()[0] == 1:
            action()

def start_game():
    pygame.quit()
    main()

def quit_game():
    sys.exit()
def show_menu():
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simulador de control de una fábrica")

        fondo = pygame.Surface(screen.get_size())
        fondo.fill(BG_COLOR)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.blit(fondo, (0, 0))

            draw_button(screen, 380, 250, 200, 100, "Comenzar", start_game)
            draw_button(screen, 380, 400, 200, 100, "Salir", quit_game)

            pygame.display.flip()

def main():
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simulador de control de una fábrica")

        fondo = load_image("Vista_planta_recorte.jpg", IMG_DIR, alpha=False)

        cinta = CintaTransportadora("CintaTransportadora.png", 100, SCREEN_HEIGHT // 2 - 25)
        robot = Robot("Robot_manipulador.png", 300, SCREEN_HEIGHT // 2 - 25)
        contenedor1 = Contenedor("contenedor.png", SCREEN_WIDTH - 150, 100)
        contenedor2 = Contenedor("contenedor.png", SCREEN_WIDTH - 150, 250)
        contenedor3 = Contenedor("contenedor.png", SCREEN_WIDTH - 150, 400)

        sprites = pygame.sprite.Group()
        sprites.add(cinta)
        sprites.add(robot)
        sprites.add(contenedor1)
        sprites.add(contenedor2)
        sprites.add(contenedor3)

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            clicked_sprites = [sprite for sprite in sprites if sprite.rect.collidepoint(mouse_pos)]

            if clicked_sprites:
                target = clicked_sprites[0]
                robot.target = target

            sprites.update()

            screen.blit(fondo, (0, 0))
            sprites.draw(screen)

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
        show_menu()
