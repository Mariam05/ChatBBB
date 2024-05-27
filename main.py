import speech_to_text
import understand_text

transcription = speech_to_text.transcribe_file('sample_audio_files/VOXTAB_Academic_audio.mp3')

while True:
	question = input('You: ')
	answer = understand_text.answer_question(question, transcription)
	print('ChatBBB: ', answer)