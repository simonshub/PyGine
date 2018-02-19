


class Player:

    # the on-map location of the player in x and y
    location = [100,100]
    # the on-map facing of the player in degrees
    facing = 0
    # a map indicating whether the player is moving in a direction
    input_map = {
        "up": False, "down": False, "left": False, "right": False, "action": "",
    }


