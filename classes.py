import random

from load_resources import *


class Card:

    def __init__(self, value: str, x: int, y: int, image: Surface, scale: tuple):
        self.val = value
        self.x = x
        self.y = y
        self.img = image
        self._scale = scale
        self._lastscaled = None
        self.side = "back"
        self.brightness = 100
        self.rect = pg.Rect(x, y, *scale)
        self.hovering = False
        self._hover_const = 1.1
        self._shadow = darken_image(self.img, 0, True)
        self_scaled_shadow = None
        self.set_scale(scale)
    def set_image(self, img: Surface):
        self.img = img
        self._lastscaled = None
        self._shadow = darken_image(self.img, 0, True)
        self.set_scale(self._scale)

    # Scaling the image
    def set_scale(self, size: tuple) -> None:
        self._scale = size
        if size != self._lastscaled:
            self._scaled_img = pg.transform.scale(self.img, size)
            self._scaled_shadow = pg.transform.scale(self._shadow, size)
            self._lastscaled = size
            self.rect = pg.Rect(self.x, self.y, *self._scale)
            self.enabled = True
    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, *self._scale)
    def get_scale(self) -> tuple:
        return self._scale

    # Forward referencing to allow Card functions to refer to its own type
    def is_match(self, card: 'Card') -> bool:
        return card.val == self.val

    def set_match(self, card: 'Card', value: str) -> None:
        self.val = value
        card.val = value
        print("2 cards now have the value:", value)

    def get_clicked(self, mx: int, my: int):
        return self.rect.collidepoint(mx, my)
    # Rendering
    def render(self, surf) -> None:
        is_hover = self.enabled and self.get_clicked(*pg.mouse.get_pos())
        if self.side == "back":
            self.set_image(pg.image.load("BACK.jpg"))
        else:
            self.set_image(darken_image(card_images[self.val], self.brightness, True))


        if is_hover and self.side == "back":
            surf.blit(self._scaled_shadow, (self.x, self.y))
            if self.hovering == False:
                self.hovering = True
                self.set_scale((self._scale[0] * self._hover_const, self._scale[1] * self._hover_const))
            surf.blit(self._scaled_img, (self.x - 5, self.y - 5))
        else:
            if self.hovering == True:
                self.hovering = False
                self.set_scale((self._scale[0] * (1/self._hover_const), self._scale[1] * (1/self._hover_const)))
            surf.blit(self._scaled_img, (self.x, self.y))


class GameWindow:
    def __init__(self, title, width, height):
        self._screen = pg.display.set_mode((width, height))
        self.running = True
        self._clock = pg.time.Clock()
    def __getattr__(self, name):
        # to allow us to directly access the screen
        if hasattr(GameWindow, name):
            return __dict__[name]
        else:
            return getattr(self._screen, name)



# Arrange the cards, assuming they are of uniform size
def arrange_cards(surf: GameWindow, cards_in_row: int, cards_in_col: int, cards_list: list):
    surf_width, surf_height = surf.get_size()
    surf_height -= 40
    spacing_x = surf_width // cards_in_row
    spacing_y = surf_height // cards_in_col
    cards_scale = cards_list[0].get_scale()
    if spacing_x < cards_scale[0] or spacing_y < cards_scale[0]:
        return False
    print("Spacing X:", spacing_x)
    y = (spacing_y - cards_scale[1]) / 2 + 40
    card_num = 0
    for i in range(cards_in_col):
        x = (spacing_x - cards_scale[0]) / 2
        for j in range(cards_in_row):
            cards_list[card_num].set_pos(x, y)
            x += spacing_x
            card_num += 1
        y += spacing_y
    return True


def randomize_card_items(cards_list: list, img_choices: list):
    cards_left = list(range(len(cards_list)))
    images_left = list(range(len(img_choices)))
    while cards_left != [] and img_choices != []:
        card1, card2 = random.sample(cards_left, 2)
        cards_left.remove(card1)
        cards_left.remove(card2)
        temp = random.choice(images_left)
        cards_list[card1].set_match(cards_list[card2], temp if images_left.remove(temp) == None else None)