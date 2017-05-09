from mpf.core.mode import Mode
from mpf.core.delays import DelayManager

class bonus_award(Mode):
  def mode_init(self):
    self.log.info('bonus award python code initalized')

  def mode_start(self, **kwargs):
    #initalize the delay manager
    self.delay = DelayManager(self.machine.delayRegistry)
    #The way this mode works, it watches for this slide to be posted:
    self.add_mode_event_handler("slide_bonus_award_1_slide_active", self.bonus_start_1)
#Then the mode runs through three different delay managers

#this is the first step, it displays the bonus award slide for 1.5 seconds before
#handing the mode over to the next step
  def bonus_start_1(self, **kwargs):
    self.log.info('bonus start 1 called')
    #this varable is needed to hold the bonus value in the next step
    #it was just convient to put it here in this method
    self.player.bonus_holder = self.player.bonus
    self.delay.add(name='bonus_1', ms=1500, callback=self.bonus_addup)

#this is the 2nd step in the bonus award.  It counts down the bonus, and
#adds the bonus to the score.  Because we are using player.bonus, and
#mode bonus is still running, the bonus lights will count down with the
#award of the bonus points, just like in the orignal game.
  def bonus_addup(self, **kwargs):
      if self.player.bonus_x > 0:
        # if we still have bonus x, we keep counting down bonus
          if self.player.bonus >0:
            self.player.score += 1000
            self.player.bonus -= 1000

            # when we run out of bonus, we lower bonus x, and reset bonus total
          else:
            self.player.bonus_x -= 1
            if self.player.bonus_x > 0:
                self.player.bonus = self.player.bonus_holder

         #we are basically running this in a loop until we run out of bonux X
          self.delay.add(name='bonus_addup', ms=50, callback=self.bonus_addup)
        #when we are out of bonus X, we stop the count down, and pause before
        #moving on..
      else:
          self.delay.add(name='last_bonus_delay', ms=1000, callback=self.last_bonus)

#this is the last step.  when this is called after the last_bonus_delay pause
#to allow the player to see the score before we pull the slide.  The event
#listed below triggers the slide player in the yaml file to remove the slide
  def last_bonus(self, **kwargs):
      self.machine.events.post('remove_bonus_award_1')
