import pygame

import network
import utils
import env
import res

def start_client():
    utils.log("Starting...")

    # initialize game
    env.Game.init()
    # initialize resources
    res.Resources.init()

    # start the client connection
    network.Client()

    utils.log("Ready!")
    while not env.Game.stopped:
        # collect events into list
        events = pygame.event.get()
        env.Game.States.get_active().update(events)

        # clear the screen
        env.Game.screen.fill((0, 0, 0))

        # render stuff
        env.Game.States.get_active().render()

        # show n tell
        pygame.display.update()

def start_server():
    utils.log("Starting...")

    # initialize game
    env.Game.init(True)

    # start the host service
    network.Server(address=network.Server.get_ip())

    utils.log("Ready!")
    while not env.Game.stopped:
        # update currently active state
        env.Game.States.get_active().update()