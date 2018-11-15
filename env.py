
import pygame
import json
import os

import states
import utils



# contains constants regarding the locations of important stuff
class Environment:

    # the file path of the settings.cfg file, relative to the current directory
    SETTINGS_FILE_PATH = "data/settings.cfg"
    # the file path of the bindings.cfg file, relative to the current directory
    BINDINGS_FILE_PATH = "data/bindings.cfg"
    # the file path of the player_info.cfg file, relative to the current directory
    PLAYER_INFO_FILE_PATH = "data/player_info.cfg"

    # the file path of sound resources, relative to the current directory
    RES_SOUNDS_PATH = "res/sounds/"
    # the file path of script resources, relative to the current directory
    RES_SCRIPTS_PATH = "res/scripts/"
    # the file path of graphic resources, relative to the current directory
    RES_GRAPHICS_PATH = "res/graphics/"



# contains camera data
class Camera:

    location = [0,0]
    zoom = 1.



# contains game data
class Game:

    DEFAULT_SCREEN_SIZE = (1280,1024)

    # this dictionary contains all the default game settings
    # at game init, if a settings file does not exist, it will
    # be created using these settings. otherwise, these
    # settings are replaced by those in the file
    settings = {
        "title": "MyGame",
        "icon": "",
        "screen_size": DEFAULT_SCREEN_SIZE,
        "fullscreen": False,
        "no_frame": False,
        "hw_acceleration": False, # requires fullscreen
    }

    bindings = {
        "quit": pygame.K_ESCAPE,
        "": None,
    }

    player_info = {
        "name": "Unknown",
        "color": [ 255,0,0 ]
    }

    stopped = False

    screen = None

    network_object = None

    @staticmethod
    def init(client=False):
        utils.log("Loading settings...")
        # check if settings file exists
        if os.path.isfile(Environment.SETTINGS_FILE_PATH):
            # exists - read it
            with open(Environment.SETTINGS_FILE_PATH) as settings_file:
                data = json.load(settings_file)
            # check whether all setting keys exist in the opened file
            bad = False
            try:
                for settings_key in Game.settings:
                    if settings_key not in data:
                        # if a key is missing, log it and recreate the default settings file
                        utils.log_wrn("Missing settings key '"+settings_key+"'! Reverting to default settings...")
                        json_data = json.dumps(Game.settings, indent=4, separators=(',',':'))
                        dump_file = open(Environment.SETTINGS_FILE_PATH, "w")
                        dump_file.write(json_data)
                        dump_file.close()
                        bad = True
                        break
            except ValueError:
                utils.log_err("Failed to read settings file; bad JSON format")
            # set settings
            if not bad:  Game.settings = data

        else:
            # does not exist - create it
            utils.log("No settings file, creating new file with defaults...")
            json_data = json.dumps(Game.settings, indent=4, separators=(',',':'))
            dump_file = open(Environment.SETTINGS_FILE_PATH, "w")
            dump_file.write(json_data)
            dump_file.close()
            utils.log_err("Failed to create default settings file!")


        utils.log("Loading bindings...")
        # check if bindings file exists
        if os.path.isfile(Environment.BINDINGS_FILE_PATH):
            # exists - read it
            with open(Environment.BINDINGS_FILE_PATH) as bindings_file:
                data = json.load(bindings_file)
            # check whether all setting keys exist in the opened file
            bad = False
            try:
                for binding_key in Game.bindings:
                    if binding_key not in data:
                        # if a key is missing, log it and recreate the default settings file
                        utils.log_wrn("Missing binding key '"+binding_key+"'! Reverting to default settings...")
                        json_data = json.dumps(Game.bindings, indent=4, separators=(',',':'))
                        dump_file = open(Environment.BINDINGS_FILE_PATH, "w")
                        dump_file.write(json_data)
                        dump_file.close()
                        bad = True
                        break
            except ValueError:
                utils.log_err("Failed to read bindings file; bad JSON format")
            # set settings
            if not bad:  Game.bindings = data

        else:
            # does not exist - create it
            utils.log("No bindings file, creating new file with defaults...")
            json_data = json.dumps(Game.bindings, indent=4, separators=(',',':'))
            dump_file = open(Environment.BINDINGS_FILE_PATH, "w")
            dump_file.write(json_data)
            dump_file.close()
            utils.log_err("Failed to create default bindings file!")

        # if the client flag is set, do not initialize pygame
        if not client:
            utils.log("Loading player info...")
            # check if player info file exists
            if os.path.isfile(Environment.PLAYER_INFO_FILE_PATH):
                # exists - read it
                with open(Environment.PLAYER_INFO_FILE_PATH) as player_info_file:
                    data = json.load(player_info_file)
                # check whether all player info keys exist in the opened file
                bad = False
                try:
                    for binding_key in Game.player_info:
                        if binding_key not in data:
                            # if a key is missing, log it and recreate the default settings file
                            utils.log_wrn("Missing player info key '"+binding_key+"'! Reverting to default settings...")
                            json_data = json.dumps(Game.player_info, indent=4, separators=(',',':'))
                            dump_file = open(Environment.PLAYER_INFO_FILE_PATH, "w")
                            dump_file.write(json_data)
                            dump_file.close()
                            bad = True
                            break
                except ValueError:
                    utils.log_err("Failed to read player info file; bad JSON format")
                # set settings
                if not bad:  Game.player_info = data

            else:
                # does not exist - create it
                utils.log("No player info file, creating new file with defaults...")
                json_data = json.dumps(Game.player_info, indent=4, separators=(',',':'))
                dump_file = open(Environment.PLAYER_INFO_FILE_PATH, "w")
                dump_file.write(json_data)
                dump_file.close()
                utils.log_err("Failed to create default player info file!")


            # initialize pygame
            utils.log("Initializing PyGame library...")
            pygame.mixer.pre_init(44100, 16, 2, 4096)
            pygame.init()
            Game.screen = pygame.display.set_mode(Game.settings["screen_size"])
            pygame.display.set_caption(Game.settings["title"])
            pygame.display.set_icon(pygame.image.load(Game.settings["icon"]))
            utils.log("PyGame library initialized!")



    # contains all the game states, and indicates the one currently active
    class States:

        # contains the key of the currently active game state
        active = "playing"

        # contains a map of all added game states - each state has it's own class in the states.py file
        states = {
            "menu": states.Gamestate_Menu(),
            "playing": states.Gamestate_Playing(),
        }

        # returns the currently active game state
        @staticmethod
        def get_active():
            return Game.States.states[Game.States.active]

        # enters the targeted game state
        @staticmethod
        def set_active(key):
            if Game.States.get(key) is not None:
                Game.States.active = key
                Game.States.get_active().enter()

        # returns the game state of the given key (name)
        @staticmethod
        def get(key):
            if isinstance(key, str) and key in Game.States.states:
                return Game.States.states[key]
            else:
                return None
