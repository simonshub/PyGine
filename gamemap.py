import env
import res



class Tile:
    # these constants point to their respectable graphics for rendering
    # since we want impathable tiles to be black, we won't even use them for rendering
    PATHABLE_TILE_GRAPHICS = "tile"
    #IMPATHABLE_TILE_GRAPHICS = ""

    # this constant is used to define the default rendering size of the tile graphics
    TILE_GRAPHICS_SIZE = (64,64)

    def __init__(self, pathable=True):
        self.pathable = pathable

    # renders the tile at the specified on-screen location
    def render(self, location):
        if self.pathable:
            res.render(res.get_grf(Tile.PATHABLE_TILE_GRAPHICS), location, size=Tile.TILE_GRAPHICS_SIZE)
        else:
            # env.render(res.get_grf(Tile.IMPATHABLE_TILE_GRAPHICS), location)
            pass



class GameMap:

    tile_map = [[]]
    width, height = 0, 0
    player_list = [ ]

    # initialize a map for editing
    def __init__(self, width, height):
        self.width = width
        self.height = height
        for y in range(height):
            self.tile_map.append([])
            for x in range(width):
                self.tile_map[y].append(Tile())

    # renders the map using the environment camera
    def render(self):
        w, h = Tile.TILE_GRAPHICS_SIZE

        for y in range(self.height):
            for x in range(self.width):
                self.tile_map[y][x].render((x*w,y*h))

        for player in self.player_list:
            player.render()
