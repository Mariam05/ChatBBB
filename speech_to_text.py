def transcribe_file(filepath):
	import whisper

	model = whisper.load_model("base")
	result = model.transcribe(filepath)
	return result["text"]

	# use faster whisper or whisper X