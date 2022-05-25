from utils import check, __file__ as ufile

BANNER = """
 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗      ██████╗██╗   ██╗██████╗ ███████╗██████╗      ██████╗██╗   ██╗██████╗ 
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║   ██║██╔══██╗
██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║    ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██║     ██║   ██║██████╔╝
██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██║     ██║   ██║██╔═══╝ 
╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ╚██████╗╚██████╔╝██║     
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝      ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝     ╚═════╝ ╚═════╝ ╚═╝     
                                                                                                                             																														 
"""

MESSAGE = """Welcome to CyberCup,
The CyberCup this weekend will be crypto crypto crypto. Through a set of independant tasks,
you'll be solving the challenges one by one. Once you solve one it will unlock the next one, and another will appear on the platform.
Solve Level 1, and Level 2 will be available and so on and so forth. You must submit the flags on the plateform.
This cup will have 8 levels with various difficulties (but winnable as @iwd suggested :) )

Ps: To guarantee that you solved the tasks in order, there will be Proof of Flag - PoF algorithm to do so.
If you want to unlock the challenge N, you need to xor all the flags of tasks 1..N-1 and submit the sha256
of the result to the level N PoF. This is called PoF and it differs of the flags you submit on the plateform. Check it's source code from the menu.

Who will complete them first will be the Winner :D
Happy hacking!
"""

def menu():
	MENU  = "\n==================== Choose a level ====================\n"
	MENU += "Select:\n"
	MENU += " 0. PoF function\n"
	MENU += " 1. Level 1\n"
	MENU += " 2. Level 2\n"
	MENU += " 3. Level 3\n"
	MENU += " 4. Level 4\n"
	MENU += " 5. Level 5\n"
	MENU += " 6. Level 6\n"
	MENU += " 7. Level 7\n"
	MENU += " 8. Level 8\n"
	MENU += "> "

	choice = input(MENU)
	return choice


def main():
	print(BANNER)
	print(MESSAGE)
	for i in range(10):
		try:
			choice = menu()
			if choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
				choice = int(choice)
				h = input("You need first to provide a PoF (hex): ")
				if check(h, choice):
					print("Correct PoF")
					
					try:
						print("-" * 100)
						with open(f"/challenge/level{choice}/desc.txt") as f:
							print(f.read())
						with open(f"/challenge/level{choice}/chall.txt") as f:
							print(f.read())
						print("-" * 100)
					except Exception as e:
						print(e)
						pass
				else:
					print("Don't hurry. Solve the previous ones before.")

			elif choice == "0":
				print("-" * 100)
				with open(ufile) as f:
					print(f.read())
				print("-" * 100)
		except Exception as e:
			print(e)
			pass

if __name__ == "__main__":
	main()

