from PIL import Image
import PIL.ImageOps
import pygame as pg
from pygame import Surface
import pygame.time
import random
pg.init()
def invert_colors(file: str) -> Surface:
    print("CURRENT INVERT:",file)
    im = Image.open(file).convert("RGB")
    r, g, b = im.split()
    r = r.point(lambda t: 255 - t)
    img = Image.merge('RGB', (g,b,r))
    img = pg.image.fromstring(img.tobytes(), img.size, img.mode)
    return img
def darken_image(file, per: int, is_pg:bool = False):
    if is_pg:
        im = pygame.image.tostring(file, "RGB", False)
        im = Image.frombytes("RGB", file.get_size(), im)
    else:
        im = Image.open(file).convert("RGB")
    r, g, b = im.split()
    r = r.point(lambda t, percent=per: (percent) * 0.01 * t)
    g = g.point(lambda t, percent=per: (percent) * 0.01 * t)
    b = b.point(lambda t, percent=per: (percent) * 0.01 * t)
    img = Image.merge('RGB', (r, g, b))
    img = pg.image.fromstring(img.tobytes(), img.size, img.mode)
    return img

background = pg.image.load("background.png") #Load the bg image
darker_background = darken_image('background.png', 60)
card_images = ['A-1.jpg', 'A-2.jpg', 'A-3.jpg', 'A-4.jpg', 'C-16.jpg', 'F-15.jpg', 'J-1.jpg', 'K-1.jpg', 'Q-1.jpg', 'S-14.jpg']
card_images = sum([[pg.image.load(file), invert_colors(file)] for file in card_images], [])


font = pygame.font.Font('freesansbold.ttf', 32)

end_screen = Surface((500,400), pg.SRCALPHA, 32)
end_screen.fill((50, 50, 50, 240))

reset_surf = Surface((130,40))
reset_surf.fill((2,100,64))
reset_surf.blit(font.render("Restart", False, (255, 255, 255)), (10,5))
reset_rect = reset_surf.get_rect()
reset_rect.x = 550
reset_rect.y = 5

quit_surf = Surface((100,40))
quit_surf.fill((2,100,64))
quit_surf.blit(font.render("Quit", False, (255, 255, 255)), (10,5))
quit_rect = quit_surf.get_rect()
quit_rect.x = 700
quit_rect.y = 5