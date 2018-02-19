import pygame

import gamemap
import env



class Gamestate_Playing:

    game_map = gamemap.GameMap(10,10)

    def __init__(self):
        self.game_map = gamemap.GameMap(10, 10)

    def enter(self):
        None

    def update(self, events=[]):
        for event in events:
            if event.type is pygame.QUIT:
                # quit game (window exit button clicked)
                env.Game.stopped = True
            elif event.type is pygame.KEYDOWN:
                # handle on-key-press logic, per key
                if event.key is env.Game.bindings["quit"]:
                    env.Game.stopped = True
                None
            elif event.type is pygame.KEYUP:
                # handle on-key-release logic, per key
                None
            elif event.type is pygame.MOUSEBUTTONDOWN:
                # handle on-mouse-press logic, per button
                None
            elif event.type is pygame.MOUSEBUTTONUP:
                # handle on-mouse-release logic, per button
                None

    def render(self):
        self.game_map.render()



class Gamestate_Menu:

    def __init__(self):
        None

    def enter(self):
        None

    def update(self, events=[]):
        for event in events:
            if event.type is pygame.QUIT:
                # quit game (window exit button clicked)
                env.Game.stopped = True
            elif event.type is pygame.KEYDOWN:
                # handle on-key-press logic, per key
                if event.key is env.Game.bindings["quit"]:
                    env.Game.stopped = True
                None
            elif event.type is pygame.KEYUP:
                # handle on-key-release logic, per key
                None
            elif event.type is pygame.MOUSEBUTTONDOWN:
                # handle on-mouse-press logic, per button
                None
            elif event.type is pygame.MOUSEBUTTONUP:
                # handle on-mouse-release logic, per button
                None

    def render(self):
        None
