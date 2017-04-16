from mpf.core.mode import Mode

#this mode class is intended to keep track of the
#number of jet bumper hits, and increase the score
#as the number of hits increase
#this could be done with logic blocks, but
#I prefer to kee this all in one mode

class jetbumpers(Mode):

    def mode_init(self):
        self.log.info('jetbumper python code initalized')

    def mode_start(self, **kwargs):
        self.log.info('jetbumper mode starting')
        # first some mode only variables
        #counts the number of hits within the mode
        self.jetcounter = 0
        #we need two player variables to use to export
        #information to slides
        #jets remain is the number of hits left
        #to move up a level.  20 is the intial value
        self.player.jetsremain = 20
        #this is the jet bumper level (starts at 1)
        self.player.jetlevel = 1

        #now to register the events that this mode
        #will be acting on, in particular the jetbumper
        #hits
        self.add_mode_event_handler("s_left_jet_bumper_active", self.jet_score)
        self.add_mode_event_handler("s_center_jet_bumper_active", self.jet_score)
        self.add_mode_event_handler("s_right_jet_bumper_active", self.jet_score)
        self.add_mode_event_handler("s_bottom_jet_bumper_active", self.jet_score)

    #this is the function that will do the meat of the game
    #time tracking
    def jet_score(self, **kwargs):
        self.log.debug('jet score called')
        #first we score
        if self.player.jetlevel == 1:
            self.player.score += 100
        elif self.player.jetlevel == 2:
            self.player.score += 1000
        elif self.player.jetlevel == 3:
            self.player.score += 5000
        elif self.player.jetlevel == 4:
            self.player.score += 10000

        #count down the hits
        self.player.jetsremain = self.player.jetsremain - 1

        #post the results
        if self.player.jetlevel < 4:
            self.machine.events.post('jetcountdown')

        if self.player.jetlevel == 4:
           self.machine.events.post('jetcountdown')
           self.machine.events.post('jets_at_max')

        # we check if we need to level up the jets:
        if self.player.jetsremain == 0:
           self.log.debug('leveling up jets, jetremain at 0')

           if self.player.jetlevel == 1:
              self.log.debug('leveling up jets to lvl 2')
              self.player.jetlevel += 1
                #this event triggers the slide
              self.machine.events.post('jet_level_increase')
                #this event triggers the light show
              self.machine.events.post('jets_lvl_2')
                #reset remains to the next level up
              self.player.jetsremain = 40

           elif self.player.jetlevel == 2:
                self.log.debug('leveling up jets to lvl 2')
                self.player.jetlevel += 1
                self.machine.events.post('jet_level_increase')
                self.machine.events.post('jets_lvl_3')
                #reset remains to the next level up
                self.player.jetsremain = 60
           else:
                #if we are at lvel 4, we are at max
                self.player.jetlevel = 4
                self.machine.events.post('jets_at_max')

            #now score the hit
