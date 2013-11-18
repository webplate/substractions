#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *

#screen settings
full_screen = False
window_size = (900, 500)

#interface style
bg_color = (255, 255, 255)
txt_color = (0, 0, 0)
txt_font = "./fonts/UbuntuMono-R.ttf"
txt_size = 20
txt_inter = 20
bug_color = (200, 200, 255)
correct_col_color = (200, 255, 200)
unexplained_color = (255, 200, 200)
incomplete_color = (0, 0, 255)

simul_txt_color = (55, 55, 55)
simul_good_color = (213, 255, 96)
simul_almost_color = (255, 195, 96)
simul_bad_color = (255, 103, 96)

note_font = "./fonts/UbuntuMono-R.ttf"
note_size = 12
note_inter = 12

#subtractions pixel dimensions
sub_dims = (3* txt_size, 5* txt_inter)

#sheet params
sheet_dims = (4,5)
sheet_offset = (300,10)
simul_sheet_offset = (sheet_offset[0] + sub_dims[0]*5, 10)

#control settings
switch_key = K_s
graph_key = K_g
next_key = K_d
prev_key = K_q
