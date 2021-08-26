from gpiozero import PWMLED, LED

class Light:

	def __init__(self, gpio_onoff, gpio_dim, intensity):
		self.dim = PWMLED(gpio_dim)
		self.onoff = LED(gpio_onoff, active_high=False)
		self.dim.value = 1 - intensity

 	def on(self):
		self.onoff.on()

	def off(self):
		self.onoff.off()
