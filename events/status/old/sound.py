#!/usr/bin/env python2
from common import Status
from common import Settings
from common import Support
import os
import time

inited = False

def status(project, args):

    try:
        import pygame
    except:
        return Status.SUCCESS
    
    global inited
    
    try:
        snd_path = "%s/sounds/%s.wav" % (os.path.split(__file__)[0], args)
        if os.path.exists(snd_path):
            if not inited:
                pygame.init()
                pygame.mixer.init()
                inited = True
            sound = pygame.mixer.Sound(snd_path)
            sound.play()
            while pygame.mixer.get_busy():
                pass
    except:
        return Status.SUCCESS

def compatible(project):
    try:
        import pygame
    except ImportError:
        return Support.MASK & ~Support.ENVIRONMENT
    return Support.MASK

