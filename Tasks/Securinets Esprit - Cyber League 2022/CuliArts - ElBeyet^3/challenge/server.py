#! /usr/bin/python3

import os
from Crypto.Util.number import *
from secrets import FLAG

BANNER = """
  _____         __   _    ___         __      
 / ___/ __ __  / /  (_)  / _ |  ____ / /_  ___
/ /__  / // / / /  / /  / __ | / __// __/ (_-<
\___/  \_,_/ /_/  /_/  /_/ |_|/_/   \__/ /___/
                                              
"""

MESSAGE = """Welcome again,
So we continue our lessons on "Tajmir El Beyet^3".
As you know a non fresh meal sucks. So, today's special is to know why?
"""

def menu():
	MENU  = "\n==================== El Menu ====================\n"
	MENU += "Select:\n"
	MENU += " 1. Jammer El Beyet^3\n"
	MENU += " 2. Quit\n"
	MENU += "> "

	choice = input(MENU)
	return choice

def encrypt(m, e, N):
	return hex(pow(m, e, N))

def jammer_elbeyet(c, d, n):
	m = pow(c,d,n)
	return m % 2

def main():
	print(BANNER)
	print(MESSAGE)

	p = getPrime(1024)
	q = getPrime(1024)
	N = p*q
	phi = (p-1)*(q-1)
	e = 65537
	d = inverse(e,phi)

	enc_flag = encrypt(bytes_to_long(FLAG),e ,N)
	print("N =",hex(N))
	print("e =",hex(e))

	print("\n\nThis is a very old meal, I cannot recognize its taste anymore (pow(flag, e, N)):", enc_flag)

	while True:
		try:
			choice = menu()
			if choice == "1":

				inp = int(input("Old Meal (hex): "), 16)

				beyet = jammer_elbeyet(inp, d, N)
				print(f"Some leftovers for you ( pow(c,d,N)%2 ): {beyet}")
				
			elif choice == "2":
				print("Bye Bye.")
				
			else:
				print("No we don't have that on the menu yet.")
			
		except Exception as e:
			print(e)
			print("Don't miss behave!")
			exit(0)
		
		finally:
			print("Bye!")

if __name__ == "__main__":
    main()
