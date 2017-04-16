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
        #for now, start with one poker light
        self.player.poker_lights = 1
        self.player.extra_ball_lit = False
        self.player.special_lit = False
        self.player.extra_ball_awarded = False
        self.player.special_awarded = False

        #the events we will be watching for:
        self.add_mode_event_handler("s_spade_ace_eject_active", self.spade_score)
        self.add_mode_event_handler("s_club_ace_eject_active", self.club_score)
        self.add_mode_event_handler("s_heart_ace_eject_active", self.heart_score)
        self.add_mode_event_handler("s_left_special_active", self.special_award)
        self.add_mode_event_handler("s_right_special_active", self.special_award)
        self.add_mode_event_handler("ball started", self.poker_light_update)

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

        if (self.player.extra_ball_lit == True and self.player.extra_ball_awarded == False):
            self.machine.events.post('extra_ball_flash')

        if  (self.player.extra_ball_lit == True and self.player.extra_ball_awarded == True):
            self.machine.events.post('extra_ball_solid')

        if self.player.extra_ball_lit == False:
            self.machine.events.post('extra_ball_off')


        if self.player.special_lit == True:
            self.machine.events.post('special_lit')
        else:
            self.machine.events.post('special_off')

        poker_light_call = 'poker_light_' + str(self.player.poker_lights)
        self.machine.events.post(poker_light_call)

    def heart_score(self, **kwargs):
        if self.player.heart_eject_made == False:
           self.player.heart_eject_made = True
           self.player.score += 10000
           #we dont off the light show here
           #because it is done in poker_check
           self.poker_check()
        else:
           self.player.score +=1000

    def club_score(self, **kwargs):
        if self.player.club_eject_made == False:
            self.player.club_eject_made = True
            self.player.score += 10000
             #we dont off the light show here
             #because it is done in poker_check
            self.poker_check()
        else:
            self.player.score += 1000

    def spade_score(self, **kwargs):
        if self.player.spade_eject_made == False:
            self.player.spade_eject_made = True
            self.player.score += 10000
             #we dont off the light show here
             #because it is done in poker_check
            self.poker_check()
        else:
            self.player.score += 1000

    def special_award(self, **kwargs):
        pass

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
            #now we check to see if we need to light up extra ball, or special

        if (self.player.poker_lights == 3 and self.player.extra_ball_awarded == False):
                 #extra ball is lit
            self.log.info("Extra Ball condition met")
            self.player.extra_ball_lit == True
        else:
            self.log.info("Extra Ball condition not met")


        self.poker_light_update()
