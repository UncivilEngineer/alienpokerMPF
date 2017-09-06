from mpf.core.mode import Mode
from mpf.core.delays import DelayManager

class royal_flush(Mode):

    def mode_init(self):
        self.log.info('royal flush code initalized')

    def mode_start(self, **kwargs):
        self.log.info('royal flush mode starting')
        #inital values
        self.player.ten_made = False
        self.player.jack_made = False
        self.player.queen_made = False
        self.player.king_made = False
        self.player.ace_made = False
        self.player.royal_flush_base = 100000
    #event handlers...
        self.add_mode_event_handler("poker_spade_eject_made", self.royal_flush_increase )
        self.add_mode_event_handler("ball_started", self.royal_reset)
        self.add_mode_event_handler("s_ten_drop_target_active", self.ten_score)
        self.add_mode_event_handler("s_jack_drop_target_active", self.jack_score)
        self.add_mode_event_handler("s_queen_drop_target_active", self.queen_score)
        self.add_mode_event_handler("s_king_drop_target_active", self.king_score)
        self.add_mode_event_handler("s_ace_drop_target_active", self.ace_score)
#this function will reset the drop target bank in sequense
        self.royal_reset()
        self.royal_flush_light_update()

    def royal_reset(self, **kwargs):
        #first we reset the varaibles
        self.log.info('royal reset called')
        #failsafe vaiable to keep the switches from scoring
        #during a reset events

        self.player.royal_score = False
        #the reason the reset event is split up in to steps is Because
        #these older machines don't take well to hitting all the coils
        #at once.
        #we pulse the reset coil, and move to step 2
        self.machine.coils.c_drop_target_release.pulse()
        self.delay.add(name='royal_reset', ms = 350, callback= self.royal_reset_2)

    def royal_reset_2(self, **kwargs):
        #this is step two of the reset process
        #now we check to see if we need to reset the Ace drop target
        #the ace always will need to be reset:
        self.machine.coils.c_ace_drop_target_reset.pulse()
        self.delay.add(name='royal_reset_2', ms = 100, callback= self.royal_reset_3)

    def royal_reset_3(self, **kwargs):
        #this is step three of the reset process
        #We check to see if the king needs to be reset
        if self.player.king_made == False:
            self.machine.coils.c_king_drop_target_reset.pulse()
        self.delay.add(name='royal_reset_3', ms = 100, callback= self.royal_reset_4)

    def royal_reset_4(self, **kwargs):
        #this is step four of the reset process
        if self.player.queen_made == False:
            self.machine.coils.c_queen_drop_target_reset.pulse()
        self.delay.add(name='royal_reset_4', ms = 100, callback= self.royal_reset_5)

    def royal_reset_5(self, **kwargs):
        #this is step five of the reset process
        if self.player.jack_made == False:
            self.machine.coils.c_jack_drop_target_reset.pulse()
        self.delay.add(name='royal_reset_5', ms = 100, callback= self.royal_reset_6)

    def royal_reset_6(self, **kwargs):
    # this is step six of the reset process
        if self.player.ten_made == False:
            self.machine.coils.c_ten_drop_target_reset.pulse()
        self.delay.add(name='royal_reset_5', ms = 100, callback= self.royal_reset_done)

    def royal_reset_done(self):
        #as a last step, re set royal_score to True
        #to enable scoring events from the drop targets.
        self.player.royal_score  = True

    def royal_flush_increase(self, **kwargs):
        if self.player.royal_flush_base < 100000:
            self.player.royal_flush_base += 20000
            self.royal_flush_light_update()
            self.machine.events.post('royal_flush_increase')

    def royal_flush_decrease(self):
        if self.player.royal_flush_base > 20000:
            self.player.royal_flush_base -= 20000
            self.royal_flush_light_update()
            self.machine.events.post('royal_flush_decrease')

    def ten_score(self, **kwargs):
        #royal score has to be true to score the target.
        #this keeps the game from giving false scoring events
        if self.player.royal_score == True:
            self.player.ten_made = True
            self.player.score += 5000
            self.player.bonus += 1000
            self.royal_flush_increase()
        else:
            return

    def jack_score(self, **kwargs):
        #royal score has to be true to score the target.
        #this keeps the game from giving false scoring events
        if self.player.royal_score == True:
            #check to see if the target to the right has scored
            if self.player.ten_made == True:
                self.player.jack_made = True
                self.player.score += 5000
                self.player.bonus += 1000
                self.royal_flush_increase()
                #if you hit the drop targets out of order...
            else:
                self.player.score += 1000
                self.royal_flush_decrease()
                self.player.royal_score = False
                self.machine.coils.c_jack_drop_target_reset.pulse()
                self.delay.add(name='jack_drop_reset', ms = 100, callback= self.royal_reset_done)

    def queen_score(self, **kwargs):
        #royal score has to be true to score the target.
        #this keeps the game from giving false scoring events
        if self.player.royal_score == True:
            #check to see if the target to the right has scored
            if self.player.jack_made == True:
                self.player.queen_made = True
                self.player.score += 5000
                self.player.bonus += 1000
                self.royal_flush_increase()
                #if you hit the drop targets out of order...
            else:
                self.player.score += 1000
                self.royal_flush_decrease()
                self.player.royal_score = False
                self.machine.coils.c_queen_drop_target_reset.pulse()
                self.delay.add(name='queen_drop_reset', ms = 100, callback= self.royal_reset_done)

    def king_score(self, **kwargs):
        #royal score has to be true to score the target.
        #this keeps the game from giving false scoring events
        if self.player.royal_score == True:
            #check to see if the target to the right has scored
            if self.player.queen_made == True:
                self.player.king_made = True
                self.player.score += 5000
                self.player.bonus += 1000
                self.royal_flush_increase()
                #if you hit the drop targets out of order...
            else:
                self.player.score += 1000
                self.royal_flush_decrease()
                self.player.royal_score = False
                self.machine.coils.c_king_drop_target_reset.pulse()
                self.delay.add(name='king_drop_reset', ms = 100, callback= self.royal_reset_done)

    def ace_score(self, **kwargs):
        #royal score has to be true to score the target.
        #this keeps the game from giving false scoring events
        if self.player.royal_score == True:
            #check to see if the target to the right has scored
            if self.player.king_made == True:
                self.player.ace_made = True
                #award royal flush value
                self.player.bonus += 10000
                self.player.score += self.player.royal_flush_x * self.player.royal_flush_base
                self.machine.events.post('royal_flush_award')
                self.player.ten_made = False
                self.player.jack_made = False
                self.player.queen_made = False
                self.player.king_made = False
                self.player.ace_made = False
                self.royal_reset()
                #if you hit the drop targets out of order...
            else:
                self.player.score += 1000
                self.royal_flush_decrease()
                self.player.royal_score = False
                self.machine.coils.c_ace_drop_target_reset.pulse()
                self.delay.add(name='ace_drop_reset', ms = 100, callback= self.royal_reset_done)

    def royal_flush_light_update(self):
        #first we turn off the royal flush lights:
        self.machine.lights.l_advance_royal_flush.off()
        self.machine.lights.l_royal_flush_20000.off()
        self.machine.lights.l_royal_flush_40000.off()
        self.machine.lights.l_royal_flush_60000.off()
        self.machine.lights.l_royal_flush_80000.off()
        self.machine.lights.l_royal_flush_100000.off()

        if self.player.royal_flush_base < 100000:
            self.machine.lights.l_advance_royal_flush.on()
        if self.player.royal_flush_base == 100000:
            self.machine.lights.l_royal_flush_100000.on()
        if self.player.royal_flush_base == 80000:
            self.machine.lights.l_royal_flush_80000.on()
        if self.player.royal_flush_base == 60000:
            self.machine.lights.l_royal_flush_60000.on()
        if self.player.royal_flush_base == 40000:
            self.machine.lights.l_royal_flush_40000.on()
        if self.player.royal_flush_base == 20000:
            self.machine.lights.l_royal_flush_20000.on()
