from Crypto.Util.number import *

flag = b"Securinets{y0u_Sh0ulD_nO7_3ncRybt_0n3_bY_OwN}"

N = getPrime(1024) * getPrime(1024)
e = 0x10001

enc = []
for mi in flag:
	enc.append(pow(mi, e, N))

print(f"{N = }")
print(f"{e = }")
print(f"{enc = }")