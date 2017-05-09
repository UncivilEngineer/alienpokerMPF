from mpf.core.mode import Mode
import random

#this is the bonus mode
#it is intended to be used to track the bonus lights
#and at the end of a ball, award the bonus
#it will also track the bonus multiplier

class bonus(Mode):
  def mode_init(self):
    self.log.info('bonus python code initalized')

  def mode_start(self, **kwargs):
    #initalized bonus Values
    self.player.bonus = 0
    self.player.bonus_x = 1
    self.player.ll_joker_on = False
    self.player.ml_joker_on = False
    self.player.ul_joker_on = False
    self.player.r_joker_on = False

    #the events the mode is watching for
    self.add_mode_event_handler("s_lower_left_joker_active", self.ll_joker_score)
    self.add_mode_event_handler("s_middle_left_joker_active", self.ml_joker_score)
    self.add_mode_event_handler("s_top_joker_active", self.ul_joker_score)
    self.add_mode_event_handler("s_right_Joker_active", self.r_joker_score)
    self.add_mode_event_handler("player_bonus", self.update_bonus_lights)
    self.add_mode_event_handler("player_bonus_total", self.update_bonus_lights)
    #this routine will handle setting up the lighted jokers
    self.joker_setup()

  def ll_joker_score(self, **kwargs):
      if self.player.ll_joker_on == True:
        self.player.bonus_x += 1
        self.player.bonus += 1000
        self.update_bonus_lights()
        self.joker_setup()
        self.machine.events.post('bonus_x_increase')
      else:
          self.player.score += 500


  def ml_joker_score(self, **kwargs):
      if self.player.ml_joker_on == True:
        self.player.bonus_x += 1
        self.player.bonus += 1000
        self.update_bonus_lights()
        self.joker_setup()
        self.machine.events.post('bonus_x_increase')
      else:
        self.player.score += 500

  def ul_joker_score(self, **kwargs):
      if self.player.ul_joker_on == True:
        self.player.bonus_x += 1
        self.player.bonus += 1000
        self.update_bonus_lights()
        self.joker_setup()
        self.machine.events.post('bonus_x_increase')
      else:
        self.player.score += 500

  def r_joker_score(self, **kwargs):
      if self.player.r_joker_on == True:
        self.player.bonus_x += 1
        self.player.bonus += 1000
        self.update_bonus_lights()
        self.joker_setup()
        self.machine.events.post('bonus_x_increase')
      else:
        self.player.score += 500

  def joker_setup(self):

      #first turn all the joker lights off
      self.machine.lights.l_lower_left_joker.off()
      self.player.ll_joker_on = False
      self.machine.lights.l_middle_left_joker.off()
      self.player.ml_joker_on = False
      self.machine.lights.l_top_left_joker.off()
      self.player.ul_joker_on = False
      self.machine.lights.l_right_joker.off()
      self.player.r_joker_on = False
      #picking a random number from 1 to 100, as an
      #interger...
      random_joker = random.randint(1,100)

      #based on the random number, we will light one of
      #the jokers
      if random_joker <= 25:
          self.player.ll_joker_on = True
          self.machine.lights.l_lower_left_joker.on()
      elif random_joker <= 50:
          self.player.ml_joker_on = True
          self.machine.lights.l_middle_left_joker.on()
      elif random_joker <= 75:
          self.player.ul_joker_on = True
          self.machine.lights.l_top_left_joker.on()
      else:
          self.player.r_joker_on = True
          self.machine.lights.l_right_joker.on()

  def update_bonus_lights(self, **kwargs):
      self.log.info("update bonus lights called")
      bonusV = self.player.bonus
      bonusX = self.player.bonus_x
      #this is the remainder value after the big lights
      #are subtracted (40k and 20k)
      #set at 0 to start
      bonusR = 0

      bonus_lights = [ self.machine.lights.l_4k_bonus,
                       self.machine.lights.l_6k_bonus,
                       self.machine.lights.l_8k_bonus,
                       self.machine.lights.l_10k_bonus,
                       self.machine.lights.l_12k_bonus,
                       self.machine.lights.l_14k_bonus,
                       self.machine.lights.l_16k_bonus,
                       self.machine.lights.l_18k_bonus ]

      bonus_x_lights = [ self.machine.lights.l_2x,
                         self.machine.lights.l_3x,
                         self.machine.lights.l_4x,
                         self.machine.lights.l_5x ]
     #first we turn them all off
      self.machine.lights.l_20k_bonus.off()
      self.machine.lights.l_40k_bonus.off()
      #turn off bonus X lights
      for lamps in bonus_x_lights:
          lamps.off()
      #now turn off the bonus counter lights
      for lamps in bonus_lights:
          lamps.off()

      #now turn on the bonus X lights
      if bonusX >= 5:
          for lamps in bonus_x_lights:
              lamps.on()
      elif bonusX >= 2:
          for x in range (0, bonusX - 1):
              bonus_x_lights[x].on()
      else:
          pass


      #the maximum value of the bonus lights is 78,000 points
      # (18k + 20k + 40k), so we take care of the top values first
      if bonusV >= 78000:
          self.machine.lights.l_20k_bonus.on()
          self.machine.lights.l_40k_bonus.on()
          for lamps in bonus_lights:
              lamps.on()
      elif bonusV >= 60000:
          self.machine.lights.l_20k_bonus.on()
          self.machine.lights.l_40k_bonus.on()
          bonusR = bonusV - 60000
      elif bonusV >= 40000:
          self.machine.lights.l_40k_bonus.on()
          bonusR = bonusV - 40000
      elif bonusV >= 20000:
          self.machine.lights.l_20k_bonus.on()
          bonusR = bonusV - 20000
      else:
          bonusR = bonusV
      #after the main lights are lit, the remainder is used
      #to light up the rest of the bonus lights (4k to 18k)
      if bonusR >= 4000:
          lampcounter = (bonusR // 2000) - 1
          for x in range (0, lampcounter):
              bonus_lights[x].on()
