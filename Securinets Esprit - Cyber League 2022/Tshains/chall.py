from base64 import b64encode

flag = b"Shi1In_cH41N_b6464_Ch41n!!"

flag = b64encode(flag)
enc = b""
for i in range(len(flag)):
	enc += bytes([flag[i] ^ flag[(i+1) %len(flag)]])
enc = b64encode(enc)
print(enc)
# Z1oYPRg5GS1qfAcHCgIJF2p7e3wKHWloaH4hIQoCMzwaFnho


