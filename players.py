import json



class Player:

    # the on-map location of the player in x and y
    location = [0,0]
    # the on-map facing of the player in degrees
    facing = 0
    # a map indicating whether the player is moving in a direction
    movement = {
        "up": False, "down": False, "left": False, "right": False,
    }



    # returns this as a json string
    def as_json(self):
        return json.dumps(self, indent=4, separators=(',',':'))
