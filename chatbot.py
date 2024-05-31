from transformers import pipeline
from termcolor import colored, cprint

def main():
	TRANSCRIPT_FILENAME = "transcript_files/fulltranscript.txt"

	qa_pipeline = pipeline("question-answering")
	
	you = colored("You", on_color="on_light_yellow")
	bbb = colored("ChatBBB", on_color="on_light_blue")

	while True:
		try:
			transcription = open(TRANSCRIPT_FILENAME, "r").read()
			question = input(you + " ")
			answer = qa_pipeline(question=question, context=transcription)
			if answer['score'] < 0.5:
				print(bbb + colored(' hmm... I don\'t know the answer to that',on_color="on_light_red"))
			else:
				print(bbb + colored(" " + answer['answer'], on_color="on_white"))
			print(answer)
		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	main()