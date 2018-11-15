
import pygame

import threading
import network
import players
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

        # update game states with event list
        env.Game.States.get_active().update(events)

        # resolve user input and send to server
        input_pkg = players.PlayerInputPackage()
        input_pkg.populate_inputs(events)
        env.Game.network_object.send(input_pkg)

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
    env.Game.network_object = network.Server(address=address, port=port)

    networking_thread = threading.Thread(target=env.Game.network_object.start)
    networking_thread.start()

    utils.log("Ready!")
    while not env.Game.stopped:
        # update currently active state
        env.Game.States.get_active().update()


#start_server("0.0.0.0",12345)
#start_client("192.168.1.1",12345)
