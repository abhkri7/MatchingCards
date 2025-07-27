#************************* MEMORY CARD GAME ************************

# Notes to NextUp:
"""
When running this code in CodeHS, for some reason sometimes it doesn't show
   the whole window at once. To fix this, please view the embedded version in https://codehs.com/sandbox/id/html-ApWJc2
   This link fixes the issue, and all it does is embed the viewer, but it works!
"""

from classes import *

MOVES = 0
MATCHES = 0
MENU_STATUS = False
LAST_MENU_CHANGE = 0

MINS_TENS = 0
MINS_UNITS = 0
SECS_TENS = 0
SECS_UNITS = 0
TIME_INCR = pg.USEREVENT + 1
GAME_OVER = False
flipped_cards = []
def reset():
    global MOVES
    global MATCHES
    global MINS_TENS
    global MINS_UNITS
    global SECS_TENS
    global SECS_UNITS
    global TIME_INCR
    global GAME_OVER
    global flipped_cards
    MOVES = 0
    MATCHES = 0

    MINS_TENS = 0
    MINS_UNITS = 0
    SECS_TENS = 0
    SECS_UNITS = 0
    TIME_INCR = pg.USEREVENT + 1
    GAME_OVER = False
    flipped_cards = []
def game():
    global flipped_cards
    #800 640
    screen = GameWindow("Matching Game", 800, 500) #Create the window
    cards_x = 5
    cards_y = 4
    cards_total = cards_x * cards_y
    min_turns = cards_total / 2
    cards_list = [Card("taco", 100, 20, card_images[0], (63,90)) for _ in range(cards_x * cards_y)]
    print(arrange_cards(screen, cards_x, cards_y, cards_list))
    randomize_card_items(cards_list, card_images)
    flipped_cards = []
    MOVES = 0
    MATCHES = 0
    MENU_STATUS = False
    LAST_MENU_CHANGE = 0

    MINS_TENS = 0
    MINS_UNITS = 0
    SECS_TENS = 0
    SECS_UNITS = 0
    TIME_INCR = pg.USEREVENT + 1
    pygame.time.set_timer(TIME_INCR, 1000)

    GAME_OVER = False
    def write_score(score):
        font_surf = font.render(f"MOVES: {score}", False, (255, 255, 255))
        screen.blit(font_surf, (10,10))
        time_surf = font.render(f"TIME: {MINS_TENS}{MINS_UNITS}:{SECS_TENS}{SECS_UNITS}", False, (255, 255, 255))
        screen.blit(time_surf, (200, 10))
        screen.blit(reset_surf, (550, 5))
        screen.blit(quit_surf, (700, 5))

    def draw_end():
        screen.blit(end_screen, (150, 120))
        font_surf = font.render("Game Over!", False, (255, 255, 255))
        screen.blit(font_surf, (300, 200))
        font_surf = font.render(f"You scored {max(round(100 / ((MOVES - min_turns)/(min_turns))), 0)} points", False, (255, 255, 255))
        screen.blit(font_surf, (240, 300))
    def basic_rendering(mousepos):
        global flipped_cards
        global LAST_MENU_CHANGE
        global MENU_STATUS
        screen.fill((0, 0, 0))
        screen.blit(darker_background, (0, 0))
        write_score(MOVES)
        i = 0
        for card in cards_list:
            card.render(screen)
            if mousepos != None:
                if card.get_clicked(*mousepos) == True and i not in flipped_cards:
                    card.side = "front"
                    card.hover = False
                    flipped_cards.append(i)
                    card.render(screen)
                if reset_rect.collidepoint(*mousepos):
                    print("COLLDIDE")
                    return 1
                if quit_rect.collidepoint(*mousepos):
                    print("COLLUDE")
                    return 2


            i += 1
        return 0
        draw_menu()

    while screen.running:
        mousepos = None
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                screen.running = False
            if evt.type == pg.MOUSEBUTTONDOWN:
                mousepos = pg.mouse.get_pos()
            if evt.type == TIME_INCR and not GAME_OVER:
                SECS_UNITS +=1
                if SECS_UNITS == 10:
                    SECS_UNITS = 0
                    SECS_TENS +=1
                if SECS_TENS == 6:
                    SECS_TENS = 0
                    MINS_UNITS += 1
                if MINS_UNITS == 10:
                    MINS_UNITS = 0
                    MINS_TENS += 1
        if (res := basic_rendering(mousepos)) > 0:
            return res
        if len(flipped_cards) == 2:
            if cards_list[flipped_cards[0]].val == cards_list[flipped_cards[1]].val:
                print("MATCH")
                cards_list[flipped_cards[0]].brightness = 20
                cards_list[flipped_cards[1]].brightness = 20
                flipped_cards = []
                MATCHES += 1
                if MATCHES == cards_x * cards_y // 2:
                    GAME_OVER = True
                    for card in cards_list:
                        card.enabled = False
                    draw_end()

            else:
                print("No Match")
                start = pygame.time.get_ticks()
                if (res := basic_rendering(mousepos)) > 0:
                    return res
                while pygame.time.get_ticks() - start < 300:
                    pg.display.update()
                    screen._clock.tick(60)
                cards_list[flipped_cards[0]].side = "back"
                cards_list[flipped_cards[1]].side = "back"
                flipped_cards = []
            MOVES += 1
        if GAME_OVER:
            draw_end()




        pg.display.update()
reset()
result = game()
while result != 2:
    reset()
    result = game()