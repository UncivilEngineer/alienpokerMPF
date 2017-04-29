from mpf.core.mode import Mode

#this mode class is intended to keep track of the
#poker lights that come on as players make the
#eject saucers.  For each time all three saucers are hit,
#one poker letter will light up.
#spelling poker lights special

class poker(Mode):

    def mode_init(self):
        self.log.info('poker python code initalized')

    def mode_start(self, **kwargs):
        self.log.info('poker mode starting')
        #Player variables, and their inital states
        self.player.heart_eject_made = False
        self.player.club_eject_made = False
        self.player.spade_eject_made = False
        self.player.ejects_remaining = 3
        #for now, start with one poker light
        self.player.poker_lights = 1
        self.player.poker_extra_ball_lit = False
        self.player.poker_extra_ball_warning = False
        self.player.special_lit = False
        self.player.special_lit_warning = False
        self.player.poker_extra_ball_awarded = False
        self.player.special_awarded = False

        #the events we will be watching for:
        self.add_mode_event_handler("s_spade_ace_eject_active", self.spade_score)
        self.add_mode_event_handler("s_club_ace_eject_active", self.club_score)
        self.add_mode_event_handler("s_heart_ace_eject_active", self.heart_score)
        self.add_mode_event_handler("s_left_special_active", self.special_award)
        self.add_mode_event_handler("s_right_special_active", self.special_award)
        self.add_mode_event_handler("ball_started", self.poker_light_update)
        #when mode first starts, we update the lights
        self.poker_light_update()

    def poker_light_update(self, **kwargs):
        self.log.info('poker light update called')
        #this function is intended to update the light associated
        #with the mode based on the player variables
        #the actual lights are handled in the yaml
        if self.player.heart_eject_made == True:
            self.machine.events.post('hearts_eject_solid')
        else:
            self.machine.events.post('hearts_eject_flash')

        if self.player.club_eject_made == True:
           self.machine.events.post('club_eject_solid')
        else:
           self.machine.events.post('club_eject_flash')

        if self.player.spade_eject_made == True:
            self.machine.events.post('spade_eject_solid')
        else:
            self.machine.events.post('spade_eject_flash')
        #updates the extra ball lits, either flash, solid, or off
        if (self.player.poker_extra_ball_lit == True and self.player.poker_extra_ball_awarded == False):
            self.machine.events.post('extra_ball_flash')
        elif (self.player.poker_extra_ball_lit == False and self.player.poker_extra_ball_awarded == True):
            self.machine.events.post('extra_ball_solid')
        else:
            self.machine.events.post('extra_ball_off')
       #updates the special lights
        if self.player.special_lit == True:
            self.machine.events.post('special_lit')
        else:
            self.machine.events.post('special_off')
        #updates the shoot again light
        if self.player.extra_balls >= 1:
            self.machine.events.post('shoot_again_lit')
        else:
            self.machine.events.post('shoot_again_off')
        #last we update the poker lights
        poker_light_call = 'poker_light_' + str(self.player.poker_lights)
        self.machine.events.post(poker_light_call)

    def heart_score(self, **kwargs):
        if self.player.heart_eject_made == False:
           self.player.heart_eject_made = True
           self.player.ejects_remaining -= 1
           self.player.score += 10000
           if self.player.ejects_remaining > 0:
              self.machine.events.post('eject_remain_slide')
        else:
           self.player.score +=1000
        #if there is an xtra ball lit, now is the time to award it
        if self.player.poker_extra_ball_lit == True:
           self.machine.events.post('award_poker_eb')
           self.player.poker_extra_ball_lit = False
           self.player.poker_extra_ball_awarded = True
           self.poker_light_update()

        self.poker_check()
        self.player.bonus +=3000


    def club_score(self, **kwargs):
        if self.player.club_eject_made == False:
            self.player.club_eject_made = True
            self.player.ejects_remaining -= 1
            if self.player.ejects_remaining > 0:
               self.machine.events.post('eject_remain_slide')
            self.player.score += 10000
        else:
            self.player.score += 1000

        #if there is an xtra ball lit, now is the time to award it
        if self.player.poker_extra_ball_lit == True:
           self.machine.events.post('award_poker_eb')
           self.player.poker_extra_ball_lit = False
           self.player.poker_extra_ball_awarded = True
           self.poker_light_update()

        self.poker_check()
        self.player.bonus += 3000


    def spade_score(self, **kwargs):
        if self.player.spade_eject_made == False:
            self.player.spade_eject_made = True
            self.player.score += 10000
            self.player.ejects_remaining -= 1
            if self.player.ejects_remaining > 0:
                self.machine.events.post('eject_remain_slide')
             #we dont off the light show here
             #because it is done in poker_check
        else:
            self.player.score += 1000

        self.poker_check()
        self.player.bonus += 3000

    def special_award(self, **kwargs):
        if self.player.special_lit == True:
            self.machine.events.post('special_award_eb')
            self.player.special_lit = False
            self.poker_light_update()
        #regardless, we award bonus for outlanes
        self.player.bonus += 3000

    def poker_check(self):
        self.log.info("Poker Check called")
        #The purpose of this function is to check the
        #status of the eject_made lights, and see
        # if we need to advance the poker lights

        if (self.player.heart_eject_made == True and self.player.spade_eject_made == True and self.player.club_eject_made == True):
            if self.player.poker_lights < 5:
                self.player.poker_lights += 1
            # we only increast poker lights up to 5.
            #at max, we always award 100,000
            self.player.score +=100000
            #now we reset the eject lights
            self.player.heart_eject_made = False
            self.player.club_eject_made = False
            self.player.spade_eject_made = False
            self.player.ejects_remaining = 3
            #now we check to see if we need to light up extra ball, or special

        #check for lit extra ball
        if (self.player.poker_lights == 3 and self.player.poker_extra_ball_awarded == False):
                 #extra ball is lit
            self.player.poker_extra_ball_lit = True
            #need to tell player extra ball is lit, it only does this once
            if self.player.poker_extra_ball_awarded == False:
               self.machine.events.post('extra_ball_lit_slide')
               self.player.poker_extra_ball_warning = True
        #light special, lits up a 5 poker hits
        if (self.player.poker_lights == 5 and self.player.special_awarded == False):
            self.player.special_lit = True
            #tell player special is lit
            if self.player.special_lit_warning == False:
               self.machine.events.post('special_lit_slide')
               self.player.special_lit_warning = True
        #last step, update lights
        self.poker_light_update()
