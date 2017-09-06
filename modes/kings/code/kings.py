from mpf.core.mode import Mode

class kings(Mode):

    def mode_init(self):
        self.log.info('kings python code initalized')

    def mode_start(self, **kwargs):
        self.log.info('kings mode starting')

        #player variable used in kings mode:
        #this one tracks the light states
        #index 0 = hearts, 1 = Clubs, 2 = Diamonds, 3 = Spades
        self.player.king_lights= [ False,
                                   False,
                                   False,
                                   False]
        self.player.royal_flush_x = 1

        #events we watch for in this mode:
        self.add_mode_event_handler("s_king_hearts_rollover_active", self.hearts_score)
        self.add_mode_event_handler("s_king_clubs_rollover_active", self.clubs_score)
        self.add_mode_event_handler("s_king_diamonds_rollover_active", self.diamonds_score)
        self.add_mode_event_handler("s_king_spades_rollover_active", self.spades_score)
        self.add_mode_event_handler("s_left_inside_rollover_active", self.inside_lane_score)
        self.add_mode_event_handler("s_flipper_lane_change_active", self.lane_change)
        self.add_mode_event_handler('s_spinner_active', self.score_spinner)

    def hearts_score(self, **kwargs):
        if self.player.king_lights[0] == False:
            self.player.king_lights[0] = True
            self.player.bonus += 1000
            self.player.score += 5000
            self.update_king_lights()
        else:
            self.player.score += 1000

    def clubs_score(self, **kwargs):
        if self.player.king_lights[1] == False:
            self.player.king_lights[1] = True
            self.player.bonus += 1000
            self.player.score += 5000
            self.update_king_lights()
        else:
            self.player.score += 1000

    def diamonds_score(self, **kwargs):
        if self.player.king_lights[2] == False:
            self.player.king_lights[2] = True
            self.player.bonus += 1000
            self.player.score += 5000
            self.update_king_lights()
        else:
            self.player.score += 1000

    def spades_score(self, **kwargs):
        if self.player.king_lights[3] == False:
            self.player.king_lights[3] = True
            self.player.bonus += 1000
            self.player.score += 5000
            self.update_king_lights()
        else:
            self.player.score += 1000

    def inside_lane_score(self, **kwargs):
        #we light one king light with this hit
        if self.player.king_lights[0] == False:
            self.player.king_lights[0] = True
        elif self.player.king_lights[1] == False:
            self.player.king_lights[1] = True
        elif self.player.king_lights[2] == False:
            self.player.king_lights[2] = True
        else:
            self.player.king_lights[3] = True

        self.update_king_lights()
        self.player.score += 5000
        self.player.bonus += 1000


    def lane_change(self, **kwargs):
        temp_array = list(self.player.king_lights)

        self.player.king_lights[0] = temp_array[3]
        self.player.king_lights[1] = temp_array[0]
        self.player.king_lights[2] = temp_array[1]
        self.player.king_lights[3] = temp_array[2]
        self.update_king_lights()

    def score_spinner(self, **kwargs):
        if self.player.royal_flush_x >= 3:
            self.player.score += 1000
        else:
            self.player.score += 100

    def update_king_lights(self):

        #first check to see if all the kings are lit
        if (self.player.king_lights[0] == True and
            self.player.king_lights[1] == True and
            self.player.king_lights[2] == True and
            self.player.king_lights[3] == True ):

            #this will flash the lits, and turn them off
            self.machine.events.post('kings_completed')
            if self.player.royal_flush_x == 4:
                self.player.score += 10000
            if self.player.royal_flush_x < 4:
                self.player.royal_flush_x += 1
            #reset the kings lights values to false
            for x in range(4):
                self.player.king_lights[x] = False
                #self.log.info('king reset called')
                #self.log.info('king[1] ' + str(self.player.king_lights[1]))

        all_king_lights = [ self.machine.lights.l_heart_king_rollover,
                            self.machine.lights.l_club_king_rollover,
                            self.machine.lights.l_diamond_king_rollover,
                            self.machine.lights.l_spade_king_rollover]

        #first we turn them all off
        for lamps in all_king_lights:
            lamps.off()

        self.machine.lights.l_royal_flush_2x.off()
        self.machine.lights.l_royal_flush_3x.off()
        self.machine.lights.l_royal_flush_4x.off()

        #note: the spinner is hardwired into the royal flush 3x lights

        #now turn on the one we want
        if self.player.king_lights[0] == True:
            all_king_lights[0].on()
        if self.player.king_lights[1] == True:
            all_king_lights[1].on()
        if self.player.king_lights[2] == True:
            all_king_lights[2].on()
        if self.player.king_lights[3] == True:
            all_king_lights[3].on()

        if self.player.royal_flush_x == 2:
            self.machine.lights.l_royal_flush_2x.on()
        if self.player.royal_flush_x == 3:
            self.machine.lights.l_royal_flush_3x.on()
        if self.player.royal_flush_x == 4:
            self.machine.lights.l_royal_flush_4x.on()
