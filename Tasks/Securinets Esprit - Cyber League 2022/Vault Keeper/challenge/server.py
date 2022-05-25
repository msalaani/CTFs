from Crypto.Util.number import getPrime, long_to_bytes, inverse, getRandomNBitInteger

flag = b"Securinets{Y0u_Sh0uld_n3veR_truSt_aNy0n3_f0r_y0uR_s3crEts}"

class RSA:
    def __init__(self):
        self.p = getPrime(512)
        self.q = getPrime(512)
        self.e = 0x10001
        self.n = self.p * self.q
        self.d = inverse(self.e, (self.p-1)*(self.q-1))
        self.DaVinciSecretPass = b"Gimme The Ultimate Secret"
    
    def sign(self, data):
        return pow(data, self.d, self.n)
    
    def verify(self, data, sig):
        return self.sign(data) == sig

def welcome():
    welcom = ""
    welcom += """
 __   __   ______     __  __     __         ______      __  __     ______     ______     ______   ______    
/\ \ / /  /\  __ \   /\ \/\ \   /\ \       /\__  _\    /\ \/ /    /\  ___\   /\  ___\   /\  == \ /\  == \   
\ \ \\'/   \ \  __ \  \ \ \_\ \  \ \ \____  \/_/\ \/    \ \  _"-.  \ \  __\   \ \  __\   \ \  _-/ \ \  __<   
 \ \__|    \ \_\ \_\  \ \_____\  \ \_____\    \ \_\     \ \_\ \_\  \ \_____\  \ \_____\  \ \_\    \ \_\ \_\ 
  \/_/      \/_/\/_/   \/_____/   \/_____/     \/_/      \/_/\/_/   \/_____/   \/_____/   \/_/     \/_/ /_/ 
                                                                                                                                                                                                     
    """
    welcom += "Leonardo is a trust paranoiac. He build a machine for authentication. He claims that is unhackable.\n"

    print(welcom)


def SignSecret(cipher):
    print("\n --------- Sign -------------")
    user_secret = int(input(" Enter a secret to sign (hex): "), 16)
    assert 0 < user_secret < cipher.n
    if cipher.DaVinciSecretPass in long_to_bytes(user_secret):
        print(" Get Lost!")
    else:
        print(" Signed secret :",hex(cipher.sign(user_secret)))

def VerifySecret(cipher):
    print("\n --------- Verify -------------")
    user_secret = int(input(" Enter a secret to verify (hex): "), 16)
    user_signature = int(input(" Enter a signature (hex): "), 16)
    vrf = cipher.verify(user_secret, user_signature)
    if vrf :
        if cipher.DaVinciSecretPass == long_to_bytes(user_secret):
            print(" You own it!")
            print(flag)
            print("RUN ...")
            exit()
        else:
            print(" Ok!")
    else:
        print(" Get Lost liar!")
    
def menu():
	print("\n ==================== Secret Keeper - Options ====================")
	print(" 1. Sign a secret")
	print(" 2. Verify a secret")
	print(" 3. Quit")

	choice = int(input("> "))

	return choice

def main():
    welcome()
    PainterVault = RSA()
    print(" N :", hex(PainterVault.n))
    print(" e :", hex(PainterVault.e))
    for i in range(4):
        try:
            choice = menu()
            if choice == 1:
                SignSecret(PainterVault)
            if choice == 2:
                VerifySecret(PainterVault)
            if choice == 3:
                print(" Bye Bye.")
                exit()
        except:
            print(' Do not miss behave! Bye.')
            exit()

if __name__ == "__main__":
    main()
