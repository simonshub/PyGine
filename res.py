import pygame
import os

import utils
import env



class Resources:

    # these dictionaries are used to store loaded resources.
    # each resource is stored in the library of it's respective
    # type (graphics, sound, script, etc...), under it's file
    # name. all files in the designated resource folder are
    # loaded.
    graphics = {  }
    sounds = {  }
    scripts = {  }

    @staticmethod
    def init ():
        utils.log("Initializing resources...")

        # go to graphics path and find all files ending with .jpg, .jpeg or .png (regardless of letter case)
        for root, dirs, files in os.walk(env.Environment.RES_GRAPHICS_PATH):
            for file in files:
                if file.lower().endswith(".png") or file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
                    # for each graphics (.png/.jpg/.jpeg) file, add it to the graphics library
                    file_name = os.path.join(root, file)
                    key = file_name[env.Environment.RES_GRAPHICS_PATH.__len__() : file_name.rfind(".")].replace("\\","/")
                    Resources.graphics[key] = pygame.image.load(file_name)
                    utils.log("Loaded graphics '"+key+"'")

        # go to sounds path and find all files ending with .wav (regardless of letter case)
        for root, dirs, files in os.walk(env.Environment.RES_SOUNDS_PATH):
            for file in files:
                if file.lower().endswith(".wav") or file.lower().endswith(".mp3"):
                    # for each sound (.wav/.mp3) file, add it to the sound library
                    file_name = os.path.join(root, file)
                    key = file_name[env.Environment.RES_SOUNDS_PATH.__len__() : file_name.rfind(".")].replace("\\","/")
                    Resources.sounds[key] = pygame.mixer.Sound(file_name)
                    utils.log("Loaded sound '"+key+"'")

        # go to scripts path and find all files ending with .py (regardless of letter case)
        for root, dirs, files in os.walk(env.Environment.RES_SCRIPTS_PATH):
            for file in files:
                if file.lower().endswith(".py"):
                    # for each python (.py) file, add it to the script library
                    file_name = os.path.join(root, file)
                    key = file_name[env.Environment.RES_SCRIPTS_PATH.__len__() : file_name.rfind(".")].replace("\\","/")
                    Resources.scripts[key] = pygame.mixer.Sound(file_name)
                    utils.log("Loaded script '"+key+"'")
