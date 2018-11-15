
import pygame
import os

import utils
import env



# tries to fetch a named graphic
def get_grf (key):
    if isinstance(key,str) and key in Resources.graphics.keys():
        return Resources.graphics[key]
    elif isinstance(key,str):
        utils.log_err("Tried to fetch graphics '"+key+"' but no such one exists")
    else:
        utils.log_err("Tried to fetch graphics but passed key was not a string")

# tries to fetch a named sound
def get_snd (key):
    if isinstance(key,str) and key in Resources.sounds.keys():
        return Resources.sounds[key]
    elif isinstance(key,str):
        utils.log_err("Tried to fetch sound '"+str(key)+"' but no such one exists")
    else:
        utils.log_err("Tried to fetch sound but passed key was not a string")

# tries to fetch a named script
def get_scr (key):
    if isinstance(key,str) and key in Resources.scripts.keys():
        return Resources.scripts[key]
    elif isinstance(key,str):
        utils.log_err("Tried to fetch script '"+str(key)+"' but no such one exists")
    else:
        utils.log_err("Tried to fetch script but passed key was not a string")

# renders something; if a string is passed, it is resolved by the resource manager
def render(what, where, scale=(1.,1.), rotation=0, size=(-1,-1)):
    if isinstance(what,str):
        what = get_grf(what)
    if size[0] > 0 and size[1] > 0:
        what = pygame.transform.scale(what, size)
    elif scale[0] > 0 and scale[1] > 0:
        new_size = (old_size*factor for old_size,factor in zip(what.get_size(),scale))
        what = pygame.transform.scale(what, new_size)
    if rotation != 0:
        what = pygame.transform.rotate(what, rotation)
    env.Game.screen.blit(what, where)

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
