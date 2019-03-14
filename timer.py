import machine
import time

class Timer:

	def __init__(self, period):
		self.timer = machine.Timer(0)
		self.period = period
		self.timers = {}

	def _start(self):
		self.timer.init(mode=self.timer.PERIODIC, period=self.period, callback=self.timer_callback)

	def _stop(self):
		self.timer.deinit()

	def timer_callback(self, timer):
		self.check()

	def check(self):
		start = time.ticks_ms()
		for deadline in sorted(self.timers):
			if time.ticks_diff(deadline, start) > 0:
				break
			for callback in self.timers[deadline]:
				callback()
		self.timers = {k:v for k,v in self.timers.items() if time.ticks_diff(k, start) > 0}

	def add(self, delay, callback):
		target = time.ticks_add(time.ticks_ms(), delay)
		if target not in self.timers.keys():
			self.timers[target] = []
		self.timers[target].append(callback)
