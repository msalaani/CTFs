#! /usr/bin/python3

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secrets import FLAG, KEY

BLOCK_SIZE = 16

BANNER = """
  _____         __   _    ___         __      
 / ___/ __ __  / /  (_)  / _ |  ____ / /_  ___
/ /__  / // / / /  / /  / __ | / __// __/ (_-<
\___/  \_,_/ /_/  /_/  /_/ |_|/_/   \__/ /___/
                                              
"""

MESSAGE = """Welcome again,
Since Romdhan is next week, and most of you
will not be at home. So we decided to teach you
some culinary skills. Today's lesson is about El Mel7 F Chorba
As you know, after a long fasting day no body wants a salty meal, so
El Mel7 needs to be "9ad 9ad" !"""



def menu():
	MENU  = "\n==================== El Menu ====================\n"
	MENU += "Select:\n"
	MENU += " 1. Tfa9ed el mel7\n"
	MENU += " 2. Quit\n"
	MENU += "> "

	choice = input(MENU)
	return choice


def encrypt(msg):
	iv = os.urandom(BLOCK_SIZE)
	cipher = AES.new(KEY, AES.MODE_CBC, iv)

	return (iv + cipher.encrypt(pad(msg, BLOCK_SIZE))).hex()

def decrypt(data):
	iv = data[:BLOCK_SIZE]
	cipher = AES.new(KEY, AES.MODE_CBC, iv)
	
	return cipher.decrypt(data[BLOCK_SIZE:])

def tfa9ed_el_mel7(data):
	try:
		unpad(decrypt(data), BLOCK_SIZE)
		return "Delicious"
	except Exception as e:
		# print(e)
		return "Meeeel7aaa"


def main():
	print(BANNER)
	print(MESSAGE)
	print("\n\nBut first here is a perfect Chroba, try to get to this level:", encrypt(FLAG))
	while True:
		try:
			choice = menu()
			if choice == "1":
				inp = bytes.fromhex(input("Check Mel7 (hex): "))
				brik = tfa9ed_el_mel7(inp)
				print("layka_'s opinion:", brik)
				continue

			elif choice == "2":
				print("Bye Bye.")
				break
			
			else:
				print("No we don't have that on the menu yet.")
		except :
			print("Don't miss behave!")
			exit(0)

if __name__ == "__main__":
    main()
