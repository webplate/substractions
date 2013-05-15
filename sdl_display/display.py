#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform, os, pygame
from display_settings import *

#Set graphic driver according to platform
system = platform.system()
if system == 'Windows':    # tested with Windows 7
   os.environ['SDL_VIDEODRIVER'] = 'directx'
elif system == 'Darwin':   # tested with MacOS 10.5 and 10.6
   os.environ['SDL_VIDEODRIVER'] = 'Quartz'

#Initialize pygame
pygame.init()
if full_screen:
    display = pygame.display.set_mode(window_size, HWSURFACE | FULLSCREEN | DOUBLEBUF)
    pygame.mouse.set_visible(False)     #hide cursor
else:
    display = pygame.display.set_mode(window_size)

pygame.event.clear()        #clear event list to ignore previous pressures
frame = 0
t0 = pygame.time.get_ticks()
last_flip = t0
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            #to check the refresh rate
            print float(pygame.time.get_ticks() - t0)/frame, "msec/frame"
            pygame.quit()
        elif event.type == KEYDOWN and event.key == switch_key :           #switch to next stimulus
            print 'down'
    display.fill(bg_color)
    #flip every 16ms only (for smooth animation, particularly on linux)
    if pygame.time.get_ticks() > last_flip + 16 :
        last_flip = pygame.time.get_ticks()
        pygame.display.flip()
        frame += 1
