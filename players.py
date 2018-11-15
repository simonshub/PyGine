
import pygame

import env



# this class is used to render a player on-screen
class Player:

    # the display name of the player
    name = "Player"

    # the drawing color of the player
    color = [ 255,0,0 ]

    # the on-map location of the player in x and y
    location = [ 100,100 ]

    # the on-map facing of the player in degrees
    facing = 0

    def __init__(self, info):
        self.name = info["name"]
        self.color = info["color"]

    # renders this players on-screen
    def render(self):
        pygame.draw.circle(env.Game.screen, self.color, self.location, 10)



# this class represents the user's own player settings, that are sent to the server upon opening a connection
class PlayerConnectionPackage:

    # the display name of the player
    name = "Player1"

    # the display color of the player
    color = [ 255,0,0 ]

    def __init__(self, info):
        self.color = info["color"]
        self.name = info["name"]



# this class contains all the information being sent to the server on each update loop.
class PlayerInputPackage:

    # this list contains all binds that have been invoked at the KEYDOWN event type
    input_press_list = [ ]
    # this list contains all binds that have been invoked at the KEYUP event type
    input_release_list = [ ]
    # contains buttons from mouse button presses from the MOUSEBUTTONDOWN event type
    mouse_press_input = [ ]
    # contains buttons from mouse button releases from the MOUSEBUTTONUP event type
    mouse_release_input = [ ]
    # contains the x and y coordinates of the mouse location for this client
    mouse_location = ( 100,100 )

    def populate_inputs(self, events):
        # clear input lists of last update
        self.input_press_list = [ ]
        self.input_release_list = [ ]
        self.mouse_press_input = [ ]
        self.mouse_release_input = [ ]

        # update mouse position
        self.mouse_location = pygame.mouse.get_pos()

        # for each event raised during this update loop
        for event in events:
            # if it's a key press...
            if event.type is pygame.KEYDOWN:
                for bind in env.Game.bindings:
                    if env.Game.bindings[bind] is event.key:
                        # get the pressed key's corresponding command, and add it to the input list
                        self.input_press_list.append(bind)
            # if it's a key release...
            elif event.type is pygame.KEYUP:
                for bind in env.Game.bindings:
                    if env.Game.bindings[bind] is event.key:
                        # get the pressed key's corresponding command, and add it to the input list
                        self.input_release_list.append(bind)
            # if it's a mouse press...
            elif event.type is pygame.MOUSEBUTTONDOWN:
                self.mouse_press_input.append(event.key)
            # if it's a mouse release...
            elif event.type is pygame.MOUSEBUTTONUP:
                self.mouse_release_input.append(event.key)
        # done - this object is ready for sending!
