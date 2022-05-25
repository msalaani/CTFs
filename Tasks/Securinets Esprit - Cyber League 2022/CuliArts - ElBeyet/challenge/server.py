#! /usr/bin/python3

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secrets import FLAG

BLOCK_SIZE = 16
KEY = os.urandom(BLOCK_SIZE)
IV = KEY

BANNER = """
  _____         __   _    ___         __      
 / ___/ __ __  / /  (_)  / _ |  ____ / /_  ___
/ /__  / // / / /  / /  / __ | / __// __/ (_-<
\___/  \_,_/ /_/  /_/  /_/ |_|/_/   \__/ /___/
                                              
"""

MESSAGE = """Welcome again,
Since Romdhan is next week, and most of you
will not be at home. So we decided to teach you
some culinary skills. Today's lesson is about the of "Tajmir El Beyet".
As you know a non fresh meal sucks. So, today's special is to know why?
"""

def menu():
	MENU  = "\n==================== El Menu ====================\n"
	MENU += "Select:\n"
	MENU += " 1. Jammer El Beyet\n"
	MENU += " 2. Quit\n"
	MENU += "> "

	choice = input(MENU)
	return choice

def encrypt(msg):
	aes_cipher = AES.new(KEY, AES.MODE_CBC, IV)
	return aes_cipher.encrypt(pad(msg, BLOCK_SIZE)).hex()

def jammer_elbeyet(data):
	aes_cipher = AES.new(KEY, AES.MODE_CBC, IV)
	return aes_cipher.decrypt(data)

def check_leak(msg):
	msg_blocks = [msg[i: i+BLOCK_SIZE] for i in range(0, len(msg), BLOCK_SIZE)]
	flag_blocks = [FLAG[i: i+BLOCK_SIZE] for i in range(0, len(FLAG), BLOCK_SIZE)]
	for msg_block in msg_blocks:
		for flag_block in flag_blocks:
			if msg_block == flag_block:
				return True
	return False

enc_flag = encrypt(FLAG)

def main():
	print(BANNER)
	print(MESSAGE)
	print("\n\nThis is a very old meal, I cannot recognize its taste anymore:", enc_flag)

	try:
		choice = menu()
		if choice == "1":

			inp = bytes.fromhex(input("Old Meal (hex): "))
			assert len(inp) % 16 == 0 and len(inp) < 64

			beyet = jammer_elbeyet(inp)

			if check_leak(beyet):
				print("No No Idi*t! You burned l3ché!")
			else:
				print("Mekla Mjamra: ", beyet.hex())
			
		elif choice == "2":
			print("Bye Bye.")
			
		else:
			print("No we don't have that on the menu yet.")
		
	except Exception as e:
		# print(e)
		print("Don't miss behave!")
		exit(0)
	
	finally:
		print("Bye!")

if __name__ == "__main__":
    main()
