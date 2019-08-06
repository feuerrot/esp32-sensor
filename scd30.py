import ustruct
import utime

CMD_START = b"\x00\x10"
CMD_STOP = b"\x01\x04"
CMD_INTERVAL = b"\x46\x00"
CMD_READY = b"\x02\x02"
CMD_READ = b"\x03\x00"
CMD_ASC = b"\x53\x06"
CMD_FRC = b"\x52\x04"
CMD_TEMP_OFFSET = b"\x54\x03"
CMD_ALTITUDE = b"\x51\x02"
CMD_FIRMWARE = b"\xD1\x00"
CMD_RESET = b"\xD3\x04"

class SCD30:
	def __init__(self, i2c, address=0x61):
		self.i2c = i2c
		self.address = address
		self.value = []

	def _read(self, location, length):
		self.i2c.writeto(self.address, location)
		return self.i2c.readfrom(self.address, length)

	def _write(self, command, data=None):
		if data:
			pass

		self.i2c.writeto(self.address, command)

	def _crc8(self, data):
		crc = 0xFF

		for elem in data:
			crc ^= elem

			for shift in range(8):
				if (crc & 0x80):
					crc = ((crc << 1) ^ 0x31) % 0x100
				else:
					crc = crc << 1

		return crc

	def check_crc(self, data):
		for offset in range(0, len(data), 3):
			if not data[offset+2] == self._crc8(data[offset:offset+2]):
				print(offset, data[offset:offset+3])
				return False
		return True

	def start(self):
		self._write(CMD_START + b"\x00\x00\x81")

	def read(self):
		ready_raw = self._read(CMD_READY, 3)
		ready_crc = self.check_crc(ready_raw)
		ready = ustruct.unpack(">H", ready_raw[0:2])[0]
		if not ready and ready_crc:
			return None

		data_raw = self._read(CMD_READ, 18)
		data_crc = self.check_crc(data_raw)
		if not data_crc:
			return None

		self.value["co2"] = ustruct.unpack(">f", data_raw[0:2] + data_raw[3:5])[0]
		self.value["temperature"] = ustruct.unpack(">f", data_raw[6:8] + data_raw[9:11])[0]
		self.value["humidity"] = ustruct.unpack(">f", data_raw[12:14] + data_raw[15:17])[0]
		self.value["timestamp"] = utime.time()

		return True

	@property
	def values(self):
		return self.value


