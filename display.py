#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform, os, threading, pygame
from display_settings import *
import bugs, graph, stats

class async_plot(threading.Thread):
    '''an thread object to launch a pyplot window in parallel
    '''
    def __init__(self, scores, all_sc):
        threading.Thread.__init__(self)
        self.scores = scores
        self.all_sc = all_sc
    def run(self):
        graph.plot_scores(self.scores, self.all_sc)
        graph.plt.show()

def pix_coord(pos, gap, max_width, surface) :
    '''returns (top,right,bottom,left) boundaries(à la CSS) of a surface
    placed on the subtraction sheet.
    -The subtraction is placed at pos (i,j), (0,0) means top left
    -within the subtraction the surface is blitted with a gap
    (horizontal,vertical) in pixels
    -max_width is the width of the longest nb in the subtraction
    (in pixels)
    '''
    i_s, j_s = pos
    h_gap, v_gap = gap
    #where are we drawing the surface on the display ?
    #align to sheet
    left, top = sheet_offset
    #align to subtraction in sheet
    gap2 = sub_dims[0] - max_width
    left, top = left + gap2 + i_s*sub_dims[0], top + j_s*sub_dims[1]
    #align to bug column
    left = left + h_gap - txt_size/2
    #align to line
    top = top + v_gap
    #set boundaries to match surface shape
    bottom = top + surface.get_height()
    right = left + surface.get_width()
    return (top,right,bottom,left)

def draw_marker(color, nb_col=1, nb_line=3, truncate=False):
    '''returns a surface filled with rgb color
    truncate = True is for a marker of less than one line
    '''
    if truncate :
        width, height = nb_col*txt_size/2, txt_size/5
    else :
        width, height = nb_col*txt_size/2, nb_line*txt_inter - txt_size/5
    marker = pygame.Surface((width,height), flags=SRCALPHA)
    marker.fill(color)
    return marker

def draw_sub(pos, n1, n2, font, result='', simul_result='',
    simul_desc=[]):
    '''Paint the subtraction with operands n1 & n2 and result
    pos is coordinates on sheet : (0,0) is the top left sub
    '''
    fly_overs=[]
    #prepare numbers
    l1 = font.render(n1, True, txt_color) #texte, antialiasing, color
    l2 = font.render(n2, True, txt_color)
    l3 = font.render(result, True, txt_color)
    l4 = font.render(simul_result, True, simul_txt_color)
    max_width = max(l1.get_width(), l2.get_width(), l3.get_width())
    max_len = max(len(n1), len(n2), len(result))
    #prepare "decorations"
    bottom_line = font.render("_"*max_len, True, txt_color)
    sign = font.render("-", True, txt_color)
    #a surface to blit the whole sub
    width = max_width + txt_size/2
    height = 4*txt_inter
    #SRCALPHA is for per pixel transparency
    surf = pygame.Surface((width,height), flags=SRCALPHA)

    i_s, j_s = pos
    #identify bugs for drawing appropriate markers
    bugs_desc = bugs.bugId(n1, n2, result)
    #draw bugs markers
    for desc in bugs_desc:
        if desc['type'] != 'subtraction' and desc['type'] != 'correct':
            if desc['type'] in ('correct_col', 'copy')  :
                color = correct_col_color
            elif desc['type'] == 'unexplained' or desc['type'] == 'over':
                color = unexplained_color
            else :
                color = bug_color
            if desc['type'] == 'incomplete' :
                #put markers on both columns of incomplete sub
                marker = draw_marker(incomplete_color, nb_col=2, truncate=True)
                gap = (width + (desc['pos']-1)*txt_size/2, 0)
                surf.blit(marker, gap)
            else :
                marker = draw_marker(color)
                gap = (width + desc['pos']*txt_size/2, txt_size/5)
                surf.blit(marker, gap)
            boundaries = pix_coord(pos, gap, max_width, marker)#buggy?
            #HACK: reference new fly-over
            #shouldn't use global var
            fly_overs.append({'type':'detection', 'box':boundaries, 'desc':desc})
    #draw simulation markers
    for i in range(len(simul_result)) :
        col_pos = -i-1
        sim_color = simul_bad_color
        if col_pos >= -len(result) :
            if (bugs.t_d.canBeInteger(result[col_pos]) 
            and bugs.t_d.canBeInteger(simul_result[col_pos])) :
                col = int(simul_result[col_pos])
                res = int(result[col_pos])
                if col == res :
                    sim_color = simul_good_color
                elif col == res-1 or col == res+1 :
                    sim_color = simul_almost_color
        #put marker on simulation column and line
        marker = draw_marker(sim_color, nb_line=1)
        gap = (width + col_pos*txt_size/2, txt_inter*3 + txt_size/5)
        surf.blit(marker, gap)        
        #reference fly-over
        boundaries = pix_coord(pos, gap, max_width, marker)
        desc = [ bug['type'] for bug in simul_desc if bug['pos'] == col_pos ]
        #HACK: reference new fly-over
        #shouldn't use global var
        fly_overs.append({'type':'simul_col', 'box':boundaries, 'desc':desc})
    #draw numbers
    surf.blit(l1, (width - l1.get_width(), 0))
    surf.blit(l2, (width - l2.get_width(), txt_inter))
    surf.blit(l3, (width - l3.get_width(), 2*txt_inter))
    surf.blit(l4, (width - l4.get_width(), 3*txt_inter))
    #draw 'minus' and 'bottom line'
    surf.blit(bottom_line, (width - bottom_line.get_width(), txt_inter))
    surf.blit(sign, (0, txt_inter))
    return surf, fly_overs

def draw_sheet(dimensions, operations, results, simul_sheet, font):
    #clear fly_overs
    fly_overs=[]
    nb_col, nb_lgn = dimensions
    width, height = sub_dims[0]*nb_col, sub_dims[1]*nb_lgn
    surf = pygame.Surface((width,height), flags=SRCALPHA)
    for i in range(nb_col):
        for j in range(nb_lgn):
            k = i+j*nb_col
            n1 = operations[k][0]
            n2 = operations[k][1]
            result = results[k]
            sub_surf, new_fos = draw_sub((i,j), n1, n2, font, result,
            simul_sheet[1][k], simul_sheet[0][k])
            fly_overs.extend(new_fos)
            #to verticaly align on right column
            gap = sub_dims[0] - sub_surf.get_width()
            pos = (gap + i*sub_dims[0], j*sub_dims[1])
            surf.blit(sub_surf, pos)
    return surf, fly_overs

#Load experimental data of subjects and protocol
data, ref, operations = bugs.r_d.load_data(bugs.parameters.dataPath,
bugs.parameters.subject_pattern, bugs.parameters.reference,
bugs.parameters.subtractions)

class subtraction_explorer():
    '''a pygame (and pyplot) app for exploring subtractions data of subjects
    '''
    def __init__(self):
        self.running = True

    def on_init(self):
        #Load experimental data of subjects and protocol
        self.data, self.operations = bugs.r_d.load_data(bugs.parameters.dataPath,
        bugs.parameters.subject_pattern, bugs.parameters.subtractions)
        if bugs.parameters.update_precomputation == True :
            #recompute the possible bugs of the sheet (no gui)
            print "Precomputing " + bugs.parameters.precomputation_file
            bugs.write_precomputations(self.operations, bugs.parameters.precomputation_file)
            return False
        #Precompute stats on whole dataset
        self.poss_sheet = bugs.read_precomputations(bugs.parameters.precomputation_file)
        self.all_sc = stats.all_scores(self.data, self.operations) #dominancy scores for all
        self.all_congruency = stats.all_congruency(self.data, self.operations, self.poss_sheet)
        self.all_perf = stats.give_percent(self.all_congruency)

        #Set graphic driver according to platform
        system = platform.system()
        if system == 'Windows':    # tested with Windows 7
           os.environ['SDL_VIDEODRIVER'] = 'directx'
        elif system == 'Darwin':   # tested with MacOS 10.5 and 10.6
           os.environ['SDL_VIDEODRIVER'] = 'Quartz'

        #Initialize pygame
        pygame.init()
        if full_screen:
            self.display = pygame.display.set_mode(window_size, HWSURFACE | FULLSCREEN | DOUBLEBUF)
            #~ pygame.mouse.set_visible(False)     #hide cursor
        else:
            self.display = pygame.display.set_mode(window_size)

        #load fonts
        self.font = pygame.font.Font(txt_font, txt_size) #name, size
        self.note_f = pygame.font.Font(note_font, note_size)

        #Preset for startup sheet
        self.subject_id = bugs.parameters.default_sub
        self.curr_subject = -1
        #list to specify 'mouse fly-overs'
        self.fly_overs = []
 
    def on_event(self, event):
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            self.running = False
        elif event.type == KEYDOWN and event.key == switch_key :
            candidate = raw_input('Enter subject id (number) : ')
            if bugs.t_d.canBeInteger(candidate) :
                candidate = int(candidate)
                if candidate < len(self.data) :
                    self.subject_id = candidate
                else :
                    print 'No such subject in '+bugs.parameters.dataPath
            else :
                print 'Enter a number...'
        elif event.type == KEYDOWN and event.key == next_key :
            if self.curr_subject+1 < len(self.data) :
                self.subject_id = self.curr_subject+1
        elif event.type == KEYDOWN and event.key == prev_key :
            if self.curr_subject-1 > -1 :
                self.subject_id = self.curr_subject-1
        elif event.type == KEYDOWN and event.key == graph_key :
            plot_win = async_plot(self.scores, self.all_sc)
            plot_win.start()

    def on_loop(self):
        if self.subject_id != self.curr_subject :
            #compute dominancies of subject
            found_bugs = bugs.subject_sheet_bugs(self.data[self.subject_id]['results'], self.operations)
            self.scores = bugs.dominancy(found_bugs, self.poss_sheet)
            #create profile of subject (most dominant bugs)
            self.dom_bugs = bugs.profile(self.scores,
            bugs.parameters.dominancy_thre, bugs.parameters.profile_size)
            #compute simulation according to profile
            simul_sheet = bugs.simulate(self.dom_bugs, self.poss_sheet)
            #congruency between simul and data
            self.perf = stats.give_percent(stats.subject_congruency(
            self.subject_id, self.data, self.poss_sheet, simul_sheet[1],
            self.operations))
            
            #recompute background sheet only if needed
            self.sheet, self.fly_overs = draw_sheet(sheet_dims, self.operations,
            self.data[self.subject_id]['results'], simul_sheet, self.font)
            self.curr_subject = self.subject_id
        #prepare sidenotes with coord,subject name, dominant bugs, info from fly-overs...
        self.notes_lst = []
        m_x, m_y= pygame.mouse.get_pos()
        sub_time = str(self.data[self.subject_id]['time']) + " minutes"
        self.notes_lst.extend([str((m_x,m_y)), 'Global'])
        self.notes_lst.extend(self.all_perf)
        self.notes_lst.extend(['Subject '+str(self.subject_id),
        self.data[self.subject_id]['path'], sub_time,
        self.data[self.subject_id]['sheet']])
        self.notes_lst.extend(self.perf)
        str_dom_bugs = [str(tupl[0])[:5]+' : '+tupl[1] for tupl in self.dom_bugs]
        self.notes_lst.extend(str_dom_bugs)
        self.notes_lst.extend(['_______',''])
        for section in self.fly_overs :
            top, right, bottom, left = section['box']
            if m_x<right and m_x>left and m_y>top and m_y<bottom :
                if section['type'] == 'detection' :
                    self.notes_lst.extend(bugs.t_d.format_bug_desc(section['desc']))
                elif section['type'] == 'simul_col' :
                    self.notes_lst.extend(section['desc'])

    def on_render(self) :
        self.display.fill(bg_color)
        self.display.blit(self.sheet, sheet_offset)
        #draw the notes
        for line_nb, line in enumerate(self.notes_lst) :
            desc = self.note_f.render(line, True, txt_color)
            self.display.blit(desc, (note_inter,note_inter*line_nb))
        #flip every 16ms only (for smooth animation, particularly on linux)
        if pygame.time.get_ticks() > self.last_flip + 16 :
            self.last_flip = pygame.time.get_ticks()
            pygame.display.flip()
            self.frame += 1

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False :
            self.running = False
        #Main loop
        self.frame = 0
        self.last_flip = pygame.time.get_ticks()
        while self.running:
            #EVENTS
            evt = pygame.event.wait()
            evts = pygame.event.get()
            evts.insert(0, evt)
            for event in evts:
                self.on_event(event)
            #EVOLUTION
            self.on_loop()
            #RENDER
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__" :
    the_app = subtraction_explorer()
    the_app.on_execute()

