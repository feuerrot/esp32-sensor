import machine
import struct

# commands
CMD_NOP       = 0x00
CMD_DIGIT_0   = 0x01
CMD_DIGIT_1   = 0x02
CMD_DIGIT_2   = 0x03
CMD_DIGIT_3   = 0x04
CMD_DIGIT_4   = 0x05
CMD_DIGIT_5   = 0x06
CMD_DIGIT_6   = 0x07
CMD_DIGIT_7   = 0x08
CMD_DECODE    = 0x09
CMD_INTENSITY = 0x0A
CMD_LIMIT     = 0x0B
CMD_SHUTDOWN  = 0x0C
CMD_TEST      = 0x0F

# CMD_MODE
DECODE_DIGIT_0 = 0x01
DECODE_DIGIT_1 = 0x02
DECODE_DIGIT_2 = 0x04
DECODE_DIGIT_3 = 0x08
DECODE_DIGIT_4 = 0x10
DECODE_DIGIT_5 = 0x20
DECODE_DIGIT_6 = 0x40
DECODE_DIGIT_7 = 0x80

# CMD_INTENSITY
INTENSITY_0  = 0x00
INTENSITY_1  = 0x01
INTENSITY_2  = 0x02
INTENSITY_3  = 0x03
INTENSITY_4  = 0x04
INTENSITY_5  = 0x05
INTENSITY_6  = 0x06
INTENSITY_7  = 0x07
INTENSITY_8  = 0x08
INTENSITY_9  = 0x09
INTENSITY_10 = 0x0A
INTENSITY_11 = 0x0B
INTENSITY_12 = 0x0C
INTENSITY_13 = 0x0D
INTENSITY_14 = 0x0E
INTENSITY_15 = 0x0F

# CMD_LIMIT
LIMIT_0 = 0x00
LIMIT_1 = 0x01
LIMIT_2 = 0x02
LIMIT_3 = 0x03
LIMIT_4 = 0x04
LIMIT_5 = 0x05
LIMIT_6 = 0x06
LIMIT_7 = 0x07

# CMD_SHUTDOWN
SHUTDOWN_ON  = 0
SHUTDOWN_OFF = 1

# CMD_TEST
TEST_OFF = 0
TEST_ON  = 1

class max7219:
	char = {
		"0": 0x7e,
		"1": 0x30,
		"2": 0x6d,
		"3": 0x79,
		"4": 0x33,
		"5": 0x5b,
		"6": 0x5f,
		"7": 0x70,
		"8": 0x7f,
		"9": 0x7b,
		"A": 0x77,
		"B": 0x1f,
		"C": 0x4e,
		"D": 0x3d,
		"E": 0x4f,
		"F": 0x47,
		"H": 0x37,
		"L": 0x0e,
		"O": 0x7e,
		"P": 0x67,
		"U": 0x3e,
		"-": 0x01,
		" ": 0x00
	}

	def __init__(self):
		self.cs = machine.Pin(5, machine.Pin.OUT)
		self.spi = machine.SPI(2)
		self.spi.init(sck=machine.Pin(18), mosi=machine.Pin(23), baudrate=1000000)
		self.set_shutdown()
		self.set_decode()
		self.set_intensity()
		self.set_limit()
		self.set_test()

	def _write(self, cmd, value):
		self.cs.value(0)
		self.spi.write(struct.pack("BB", cmd, value))
		self.cs.value(1)

	def set_decode(self, mode=False):
		if mode:
			self._write(
				CMD_DECODE,
				DECODE_DIGIT_0 |
				DECODE_DIGIT_1 |
				DECODE_DIGIT_2 |
				DECODE_DIGIT_3 |
				DECODE_DIGIT_4 |
				DECODE_DIGIT_5 |
				DECODE_DIGIT_6 |
				DECODE_DIGIT_7
			)
		else:
			self._write(
				CMD_DECODE,
				0
			)

	def set_intensity(self, intensity=None):
		self._write(
			CMD_INTENSITY,
			intensity or INTENSITY_15
		)
	
	def set_limit(self, limit=None):
		self._write(
			CMD_LIMIT,
			limit or LIMIT_7
		)

	def set_shutdown(self, shutdown=None):
		self._write(
			CMD_SHUTDOWN,
			shutdown or SHUTDOWN_OFF
		)

	def set_test(self, test=None):
		self._write(
			CMD_TEST,
			test or TEST_OFF
		)

	def write_char(self, position, char):
		if char not in self.char:
			char = " "
		self._write(
			8 - position,
			self.char[char]
		)

	def write_string(self, string):
		if not string:
			raise Exception
		if len(string) > 8:
			raise Exception
		for pos in range(len(string)):
			self.write_char(pos, string[pos])

	def clear(self):
		self.write_string("        ")
