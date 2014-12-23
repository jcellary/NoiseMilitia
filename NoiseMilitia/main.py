
import pyaudio
import struct
import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from NoiseMilitia.cast import ChromeCast


CHUNK = 441 
CHUNK_GROUP_SIZE = 100
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SHORT_NORMALIZE = (1.0/32768.0)
NOISE_THRESHOLD = 0.03
RMS_HISTORY_TO_LOOK = 2 
WARN_DELAY = 3

class NoiseMilitia(object):
	cast = ChromeCast()
	last_rms = [] 

	def get_rms(self, block ):
		count = len(block)/2
		format = "%dh"%(count)
		shorts = struct.unpack( format, block )

		sum_squares = 0.0
		for sample in shorts:
			n = sample * SHORT_NORMALIZE
			sum_squares += n*n

		return math.sqrt( sum_squares / count )

	def process_rms(self, rms):
	
		print("RMS: %f" % rms)
		
		self.last_rms.append(rms) 
		if len(self.last_rms) == RMS_HISTORY_TO_LOOK:
			self.last_rms = self.last_rms[1:]

			rms_average = sum(self.last_rms) / len(self.last_rms)
			if rms_average > NOISE_THRESHOLD:
				print("Exceeded!!!")
				self.cast.display_warning()
				self.last_rms = self.last_rms[WARN_DELAY:]

	def start(self):
		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
        	        channels=CHANNELS,
                	rate=RATE,
	                input=True,
        	        frames_per_buffer=CHUNK)

		count = 0
		rms_average = 0.0
		while True:
			try:
				data = stream.read(CHUNK)

				rms = self.get_rms(data)
	
				if count % CHUNK_GROUP_SIZE == 0:
					self.process_rms(rms_average)
					count = 0
				rms_average = (rms_average * count + rms) / (count + 1)	
				count += 1
			except IOError:
				print("IOError")

		stream.stop_stream()
		stream.close()
		p.terminate()

if __name__ == "__main__":
	nm = NoiseMilitia()
	nm.start()
