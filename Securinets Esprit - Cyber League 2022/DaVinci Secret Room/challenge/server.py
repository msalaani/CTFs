from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import random
import os

BLOCK_SIZE = 16
KEY = os.urandom(BLOCK_SIZE)
FLAG = b"Securinets{CongratZzZzZ_y0u_g0t_inTo_tH3_DaV1nci_s3cr3t_R0om}"

def encrypt(msg):
	iv = os.urandom(BLOCK_SIZE)
	cipher = AES.new(KEY, AES.MODE_CBC, iv)
	return (iv + cipher.encrypt(pad(msg, BLOCK_SIZE))).hex()


def decrypt(data):
	iv = data[:BLOCK_SIZE]
	cipher = AES.new(KEY, AES.MODE_CBC, iv)
	return unpad(cipher.decrypt(data[BLOCK_SIZE:]), BLOCK_SIZE)

def parse(enc_token):
	dec = decrypt(enc_token)
	splitted_token = dec.split(b"|")
	assert len(splitted_token) == 2, "Please enter a token in the format encrypt(name|rm=int)"
	assert splitted_token[1].startswith(b"rm="), "no room is found"
	name, room = splitted_token[0], splitted_token[1][3:].decode()
	return name, int(room)

def menu():
	print("\n==================== DaVinci House - Entry ====================")
	print("1. Show Rooms")
	print("2. Get Room Access Token")
	print("3. Enter Room")
	print("4. Quit")

	choice = int(input("> "))

	return choice

def showRooms():
	print("\n*** Davinci House - Available Rooms ***")

	print("  Room 1: Monalisa Room")
	print("  Room 2: The Last Supper Room")
	print("  Room 3: Vitruvian Man Room")
	print("  Room 4: Salvator Mundi Room")
	print("  Room 1337: Secret Room")

def getRoomAccess():
	print("*** DaVinci House - Registration Gate ***")

	name = input("Name : ").encode()
	assert not b"davinci" in name.lower(), "No you're Not DaVinci, FRAUD!"

	room = int(input("Room number : "))
	assert 1 <= room <= 4, "Where you think can go ?"
	token = name + b"|" + b"rm=" + str(room).encode()

	return encrypt(token)

def enterRoom():
	print("\n*** Davinci House - Enter a Room ***")
	token = bytes.fromhex(input("Give your secret token (hex): "))
	name, room = parse(token)
	if name == b"DaVinci":
		if room == 1337:
			print("You made the impossible! Welcome to DaVinci's secret room, now take this ...")
			print(FLAG)
			print("And RUUN!")
			exit()
		else:
			print("Yeah Davinci can go anywhere in his house!\n")
	else:
		if room == 1337:
			print("Get lost!\n")
		else:
			print(f"Welcome to room {room}, enjoy !\n")


def welcome():
	welcome = "Welcome to"
	welcome += """
    ___               _               _                                  
   /   \ __ _ /\   /\(_) _ __    ___ (_)   /\  /\ ___   _   _  ___   ___ 
  / /\ // _` |\ \ / /| || '_ \  / __|| |  / /_/ // _ \ | | | |/ __| / _ \\
 / /_//| (_| | \ V / | || | | || (__ | | / __  /| (_) || |_| |\__ \|  __/
/___,'  \__,_|  \_/  |_||_| |_| \___||_| \/ /_/  \___/  \__,_||___/ \___|
                                                                         
"""

	welcome += "\nDaVinci gives you the one and only opportunity to visit his house"
	welcome += "\nAnd discover his paintings. All the his work is divided into 5 rooms."
	welcome += "\nBut there is one room that he refused to open."

	print(welcome)

def main():
	welcome()


	for i in range(3):
		try:
			choice = menu()
			if choice == 1:
				showRooms()

			if choice == 2:
				enc_token = getRoomAccess()
				print("Here is your token, use it carefully:", enc_token)

			if choice == 3:
				enterRoom()
			if choice == 4:
				print("\nSee next time!")
				exit()
		except:
			print("\nDon't cause problems. Bye!")
			exit()
	
if __name__ == "__main__":
	main()
