import pdfplumber
import random
from os import listdir
from os.path import isfile, join
import re
import io

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def make_quiz(folder,numQuiz):
	quizzes = []
	qPerChapter = 5

	onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
	onlyFiles = natural_sort(onlyfiles)
	
	for file in onlyfiles:
		quizzes.append(getRandomQuesions(folder+file,qPerChapter,numQuiz))

	answers = 'Answers: \n'

	for i in range(1,numQuiz+1):
		counter = 1
		with io.open("quizzes/test"+str(i)+".txt", "w", encoding="utf-8") as f:
			
			for chapter in quizzes:
				for q in chapter[(i-1):(i-1+qPerChapter)]:
					f.write(str(counter)+". "+q[0]+"\n")
					answers += str(counter)+". "+q[1]+"\n"
					counter += 1

			f.write("\n\n"+answers)

def getRandomQuesions(file,numQuestions,numQuiz):
	
	pdf = pdfplumber.open(file)
	questions = []
	q_text = ''

	for page in pdf.pages:
		text = page.extract_text()

		lines = text.split("\n")[2:]		

		for line in lines:
			line = line.replace("\xa0"," ")
			if 'CopyrightCengage' in line:
				continue
			elif "ANSWER" not in line:
				q_text += line + "\n"
			else:
				try:
					questions.append([q_text.split(" ",1)[1],line])
				except IndexError:
					pass
				q_text = ''

				if len(questions) > 100:
					break

	
	pdf.close()
	print("Done "+file)

	return random.sample(questions,numQuestions*numQuiz)


		


if __name__ == '__main__':
	path = 'MC Questions/'
	numQuiz = 5
    
	make_quiz(path,numQuiz)