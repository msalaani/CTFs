import hashlib, random, signal, sys
from time import sleep
from secrets import questions_pool, flag

TIMEOUT = 8

def handle_timeout(signum, frame):
	print("No Answer!!!!!!\nChef: Yo! We don't have all the night!\nBye!")
	sys.exit(0)
	
signal.signal(signal.SIGALRM, handle_timeout)

def hash(plaintext):
	return bin(int(hashlib.sha256(plaintext).hexdigest(), 16))[2:]

def gen(qsts_pool, answers_pool = [b"Yes", b"No"]):

	random.shuffle(qsts_pool)

	qsts = random.sample(qsts_pool, 30)
	answers = [random.choice(answers_pool) for _ in range(30)]

	answers_hashes = [hash(answer) for answer in answers]

	return qsts, answers_hashes

def check(plaintext, hashcode, redundancy_check = 100000):
	good = True
	for _ in range(redundancy_check):
		for b1,b2 in zip(hash(plaintext), hashcode):
			good &= ( b1 == b2)
			if not good:
				return good
	return good

BANNER = """
  _____         __   _    ___         __      
 / ___/ __ __  / /  (_)  / _ |  ____ / /_  ___
/ /__  / // / / /  / /  / __ | / __// __/ (_-<
\___/  \_,_/ /_/  /_/  /_/ |_|/_/   \__/ /___/
                                              
"""

MESSAGE = """Welcome again,
And our lessons on CuliArts are still continuing. We decided to make a quiz (Tchanchina) about the mad chef's life
and whoever win it he will reveal, unfortunately for him, his secret recipe.
It seems like that idea didn't please our chef and I think he'll be
very happy if you do not answer correctly. He likes it or not, layka_ is the boss
here, he has to answer your questions!

Please answer the following Yes/No questions to win the contest. Type either "Yes" or "No" for each (without the double quotes):
"""

def quiz(questions, answers_hashes):
	win  = True
	print("===================")
	print("    BEGIN QUIZ     ")
	print("===================")
	qst_i = 1
	for question, answer_hash in zip(questions, answers_hashes):
		signal.alarm(TIMEOUT)
		u_answer = input(f"{qst_i}. " + question + "> ")
		signal.alarm(0)
		if u_answer in ["Yes", "No"]:
			win &= check(u_answer.encode(), answer_hash, 90000)
		
		else:
			win &= 0
			print("Chef: I said Yes or No Questions. Idiot!!!\nGo to next question! But I suggest you restart :3")
		qst_i += 1
	if win == True:
		print("\nChef: (⋋▂⋌)\nlayka_: You answered all questions correctly!!!")
		print("Our chef is veeeery mad now! He is hesitating giving you his secret recipe!!")
		sleep(10)
		print(f"Sorry for the dealay.\nYou earned it! Our chef's gift: {flag}")
		sys.exit(0)
	else:
		print("\nYou know that you're a big loser!\nAGAAAAAAAAAIN\n")


if __name__ == "__main__":
	qsts, ans_h = gen(questions_pool)
	print(BANNER)
	print(MESSAGE)
	for _ in range(10):
		try:
			quiz(qsts, ans_h)
		except Exception as e:
			print("\nChef: Missbehave again!!\nYeah you better don't get back. I don't want to share my secret with anybody!")
			sys.exit(0)
	print("\nDone Tries ! If you do not get the flag at this point just quit!\n")
	sys.exit(0)
		