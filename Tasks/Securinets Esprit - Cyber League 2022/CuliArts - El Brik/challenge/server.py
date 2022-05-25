#! /usr/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secrets import FLAG, KEY

BANNER = """
  _____         __   _    ___         __      
 / ___/ __ __  / /  (_)  / _ |  ____ / /_  ___
/ /__  / // / / /  / /  / __ | / __// __/ (_-<
\___/  \_,_/ /_/  /_/  /_/ |_|/_/   \__/ /___/
                                              
"""

MESSAGE = """Welcome,
Since Romdhan is next week, and most of you
will not be at home. So we decided to teach you
some culinary skills. Today's lesson is about EL BRIK
Today's special is Brik b Thon !"""



def menu():
	MENU  = "\n==================== El Menu ====================\n"
	MENU += "Select:\n"
	MENU += " 1. Brik 3adi\n"
	MENU += " 2. Brik Thon\n"
	MENU += " 3. Quit\n"
	MENU += "> "

	choice = input(MENU)
	return choice

BLOCK_SIZE = 16
aes_cipher = AES.new(KEY, AES.MODE_ECB)

def brik_3adi(cipher, msg):
	return cipher.encrypt(pad(bytes.fromhex(msg), BLOCK_SIZE)).hex()

def brik_thon(cipher, msg):
	return cipher.encrypt(pad(bytes.fromhex(msg) + FLAG, BLOCK_SIZE)).hex()

def main():
	print(BANNER)
	print(MESSAGE)
	while True:
		try:
			choice = menu()
			if choice == "1":
				inp = input("Make your brik (hex): ")
				brik = brik_3adi(aes_cipher, inp)
				print("Your brik is ready: ", brik)
				continue

			elif choice == "2":
				inp = input("Make your brik Thon (hex): ")
				brik = brik_thon(aes_cipher, inp)
				print("Your brik is ready: ", brik)
				continue

			elif choice == "3":
				print("Bye Bye.")
				exit(0)
			else:
				print("No we don't have that on the menu yet.")
		except :
			print("Don't miss behave. Bye")
			exit(0)

if __name__ == "__main__":
    main()
