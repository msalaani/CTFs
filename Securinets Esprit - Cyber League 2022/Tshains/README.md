# Tshains

##### Solves: 8
##### Points: 451

## Description
```
lag = b64encode(flag)
enc = b""
for i in range(len(flag)):
	enc += bytes([flag[i] ^ flag[(i+1) %len(flag)]])
enc = b64encode(enc)
# Z1oYPRg5GS1qfAcHCgIJF2p7e3wKHWloaH4hIQoCMzwaFnho
```

Ps: Wrap what you find in the flag format Securinets{}<br>
> layka_


