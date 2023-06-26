from hashlib import sha256
from flags import flags 

# CyberCup flag is the first one in the list
# The list contains only the hex part of the flag without Securinets{}

def xor (a, b):
    return bytes(_a ^ _b for _a, _b in zip(a, b))

# NO HACKING HERE
# This is some kind of method to check if you solved the tasks in order.
# Once you start solving
# Use this function to generate hashes to unlock the next levels
def check(user_hash, n):
    res = b"\x00" * 60
    for i in range(n):
        res = xor(res, flags[i])
    res = sha256(res).hexdigest()
    #print(res)
    return res == user_hash
