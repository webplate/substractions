#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame.locals import *

#screen settings
full_screen = False
window_size = (800, 400)


#interface style
bg_color = (255, 255, 255)
txt_color = (0, 0, 0)
txt_font = "./fonts/UbuntuMono-R.ttf"
txt_size = 24
txt_inter = 24

note_font = "./fonts/UbuntuMono-R.ttf"
note_size = 12
note_inter = 12

#subtractions pixel dimensions
sub_dims = (5* txt_size, 4* txt_inter)

#sheet params
sheet_dims = (4,5)
sheet_offset = (300,10)

#control settings
switch_key = K_s
