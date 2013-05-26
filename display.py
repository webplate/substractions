#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform, os, pygame
from display_settings import *
import bugs

def draw_marker(color):
    width, height = txt_size/2, 3*txt_inter
    marker = pygame.Surface((width,height), flags=SRCALPHA)
    marker.fill(bug_color)
    return marker

def draw_sub(n1, n2, result=''):
    #prepare numbers
    l1 = font.render(n1, True, txt_color) #texte, antialiasing, color
    l2 = font.render(n2, True, txt_color)
    l3 = font.render(result, True, txt_color)
    max_width = max(l1.get_width(), l2.get_width(), l3.get_width())
    max_len = max(len(n1), len(n2), len(result))
    #prepare "decorations"
    bottom_line = font.render("_"*max_len, True, txt_color)
    sign = font.render("-", True, txt_color)
    #a surface to blit the whole sub
    width = max_width + txt_size/2
    height = 3*txt_inter
    #SRCALPHA is for per pixel transparency
    surf = pygame.Surface((width,height), flags=SRCALPHA)

    #identify bugs for drawing appropriate markers
    bugs_desc = bugs.bugId(n1, n2, result)[1]
    print bugs_desc
    #draw markers
    for desc in bugs_desc:
        if desc['type'] != 'subtraction' :
            if desc['type'] != ['unexplained'] :
                marker = draw_marker(bug_color)
                gap = width + desc['pos']*txt_size/2
                surf.blit(marker, (gap, 0))
    #draw numbers
    surf.blit(l1, (width - l1.get_width(), 0))
    surf.blit(l2, (width - l2.get_width(), txt_inter))
    surf.blit(l3, (width - l3.get_width(), 2*txt_inter))
    #draw 'minus' and 'bottom line'
    surf.blit(bottom_line, (width - bottom_line.get_width(), txt_inter))
    surf.blit(sign, (0, txt_inter))
    return surf

def draw_sheet(dimensions, operations, results):
    nb_col, nb_lgn = dimensions
    width, height = sub_dims[0]*nb_col, sub_dims[1]*nb_lgn
    surf = pygame.Surface((width,height), flags=SRCALPHA)
    for i in range(nb_col):
        for j in range(nb_lgn):
            k = i+j*nb_col
            n1 = operations[k][0]
            n2 = operations[k][1]
            result = results[k]
            sub_surf = draw_sub(n1, n2, result)
            #to verticaly align on right column
            gap = sub_dims[0] - sub_surf.get_width()
            pos = (gap + i*sub_dims[0], j*sub_dims[1])
            surf.blit(sub_surf, pos)
    return surf


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

#~ pygame.event.clear()        #clear event list to ignore previous pressures

#load  fonts
font = pygame.font.Font(txt_font, txt_size) #name, size
note_f = pygame.font.Font(note_font, note_size)

#Main loop
subject_id = bugs.default_sub
curr_subject = -1
frame = 0
t0 = pygame.time.get_ticks()
last_flip = t0
running = True
while running:
    display.fill(bg_color)
    #recompute background sheet only if needed
    if subject_id != curr_subject:
        sheet = draw_sheet(sheet_dims, bugs.operations, bugs.data[subject_id]['results'])
        curr_subject = subject_id
    display.blit(sheet, sheet_offset)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            #to check the refresh rate
            print float(pygame.time.get_ticks() - t0)/frame, "msec/frame"
            running = False
        elif event.type == KEYDOWN and event.key == switch_key :
            print 'down'
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
    #show sidenotes
    coord = note_f.render(str(pygame.mouse.get_pos()), True, txt_color)
    display.blit(coord, (10,10))
    #flip every 16ms only (for smooth animation, particularly on linux)
    if pygame.time.get_ticks() > last_flip + 16 :
        last_flip = pygame.time.get_ticks()
        pygame.display.flip()
        frame += 1
pygame.quit()
