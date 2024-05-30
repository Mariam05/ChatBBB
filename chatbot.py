from transformers import pipeline

def main():
	TRANSCRIPT_FILENAME = "transcript_files/fulltranscript.txt"

	qa_pipeline = pipeline("question-answering")

	while True:
		try:
			transcription = open(TRANSCRIPT_FILENAME, "r").read()
			question = input('You: ')
			answer = qa_pipeline(question=question, context=transcription)
			print('ChatBBB: ', answer['answer'])
		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	main()