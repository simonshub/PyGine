import pygame

import gamemap
import utils
import env
import res

utils.log("Starting...")

# initialize game
env.Game.init()
# initialize resources
res.Resources.init()

utils.log("Ready!")
while not env.Game.stopped:
    # collect events into list
    events = pygame.event.get()

    # to-do: this part should be delegated to the currently running game state !
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

    # clear the screen
    env.Game.screen.fill((0, 0, 0))

    # render stuff
    game_map.render()

    # show n tell
    pygame.display.update()