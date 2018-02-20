import pygame

import threading
import network
import utils
import env
import res

def start_client(address=None, port=None):
    utils.log("Starting...")

    # initialize game
    env.Game.init()
    # initialize resources
    res.Resources.init()

    # start the client connection
    if address is None and port is None:
        env.Game.network_object = network.Client()
    elif address is None:
        env.Game.network_object = network.Client(port=port)
    elif port is None:
        env.Game.network_object = network.Client(address=address)
    else:
        env.Game.network_object = network.Client(address=address, port=port)

    networking_thread = threading.Thread(target=env.Game.network_object.start)
    networking_thread.start()

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

def start_server(address=None, port=None):
    utils.log("Starting...")

    # initialize game
    env.Game.init(True)

    # start the host service
    if address is None and port is None:
        env.Game.network_object = network.Server()
    elif address is None:
        env.Game.network_object = network.Server(port=port)
    elif port is None:
        env.Game.network_object = network.Server(address=address)
    else:
        env.Game.network_object = network.Server(address=address, port=port)

    networking_thread = threading.Thread(target=env.Game.network_object.start)
    networking_thread.start()

    utils.log("Ready!")
    while not env.Game.stopped:
        # update currently active state
        env.Game.States.get_active().update()