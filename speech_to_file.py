from threading import Thread
from queue import Queue # will let us pass messages between threads
import pyaudio
import json
from vosk import Model, KaldiRecognizer

def main():

	recordings = Queue() # will store audio from mic and pass it to transcription
	TRANSCRIPT_FILENAME = "transcript_files/fulltranscript.txt"

	# delete contents of transcription file upon starting/restarting the program
	f = open(TRANSCRIPT_FILENAME, "w") 
	f.write('')
	f.close()

	# constants that will allow for optimal conditions for speech recognition
	CHANNELS = 1
	FRAME_RATE = 16000 # Determines how high quality the frame rate is. how quickly the audio signal is sampled. unit is kHz = cycles/sec?
	RECORD_SECONDS = 3 # How many seconds we want to record audio for before we send it off for transcription. every 20s we'll generate a transcript
	AUDIO_FORMAT = pyaudio.paInt16

	def start_threads():
		print('starting recording...')

		# thread that will record microphone
		record = Thread(target=record_microphone) 
		record.start()

		# thread that will start transcribing
		transcribe = Thread(target=speech_recognition)
		transcribe.start()

	def record_microphone(chunk=1024): # chunk is how often we are going to read audio from the microphone (how many audio frames).
		p = pyaudio.PyAudio()

		stream = p.open(format=AUDIO_FORMAT,
                    channels=CHANNELS,
                    rate=FRAME_RATE,
                    input=True,
                    # input_device_index=5,
                    frames_per_buffer=chunk)
                    
		frames = [] # will store all the audio recorded from the microphone

		while True:
			try:
				data = stream.read(chunk)
				frames.append(data)

				# if we recorded more than RECORD_SECONDS seconds of audio, then add audio data to recordings queue
				if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk: 
						recordings.put(frames.copy())
						frames = []
			except KeyboardInterrupt:
				stream.stop_stream()
				stream.close()
				p.terminate()
				break

	model = Model(model_name="vosk-model-en-us-0.22")
	rec = KaldiRecognizer(model, FRAME_RATE) # responsible for managing the audio transcription 
	rec.SetWords(True) # will give us confidence levels for each individual word

	def speech_recognition():
		while True:
			try:
				frames = recordings.get()
				raw_audio_data = b''.join(frames)

				rec.AcceptWaveform(raw_audio_data) # join all chunks together into one binary string
				result = rec.Result()
				text = json.loads(result)["text"]

				print(text)

				# write to file
				f = open(TRANSCRIPT_FILENAME,"a")
				f.write(text)
				f.close()
			except KeyboardInterrupt:
				break


	start_threads()


if __name__ == "__main__":
    main()