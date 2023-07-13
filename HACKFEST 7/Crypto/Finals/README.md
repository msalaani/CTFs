# **INTRO**
HACKFEST is one of the biggest cyber security events in Tunisia. This year we host the 7th edition of HACKFEST. This is the cryptography tasks author writeups.

# **CRYPTO - ALO**

## **TASK**
#### Points: **484**
#### Solves: **2**
#### Description


> Alo alo .. Alo ya 7obi finek !
>* [alo.py](https://github.com/msalaani/CTFs/blob/master/Hackfest%207%20-%202023/Finals/Crypto/ALO/alo.py)


```python
#!/usr/bin/env python3
from Crypto.Util.number import *
from secret import *

nbits = 1024
p, q = [getPrime(nbits) for _  in "01"]

N = p * q
phi = (p - 1) * (q - 1)

while True:
    er = getRandomInteger(nbits // 2)
    r = getRandomInteger(nbits // 2)
    if GCD(er, phi) == 1:
        dr = inverse(er, phi)
        d = dr + r
        if GCD(d, phi) == 1:
            e = inverse(d, phi)
            break

c = pow(bytes_to_long(flag), e, N)

print(f"{N = }")
print(f"{e = }")
print(f"{er = }")
print(f"{r = }")
print(f"{c = }")

"""
N = ...
e = ...
er = ...
r = ...
c = ...
"""
```
## **SOLUTION**
### Challenge
We are given RSA parameters $(N, e)$, other parameters $(e_{r}, r)$ from **YKLM** key generation, and the RSA encrypted flag.

### Analysis
The first observation is that the private exponent $d$ has a special structure. Let's analyse the key generation how it is done. This scheme was introduced as a countermeasure of CRT-Based Fault attacks on RSA.
#### **Key generation**
1. Generate two different, random large primes of the same bit-size $p$ and $q$, then calculate the **modulus** $N = pq$. $N$ has a bit-size $nbits$
2. Fixing a bound $B$ such that $B \ll N$. In the script, I chosed $B = 2^\frac{nbits}{4}$. Choosing  random **small parameters** $e_{r}$ and $r$ from $[1, B]$ where $gcd(e_{r}, \phi(N))=1$. Compute $d_{r}= e_{r}^{-1} \mod \phi(N)$
3. Compute the **secret exponent** $d = d_{r} + r$ such that $gcd(d, \phi(N))=1$
4. Compute the **public exponent** $e=d^{-1} \mod \phi(n)$

The authors said that that the parameters $e_{r}$ and $r$ can be public.

#### **Analysis of key generation**
Given $N, e, e_{r}, r$, one can obtain a multiple of $\phi(N)$.

**_Proof_ :**

The RSA equation that links the public and secret exponent is: $ed = 1 \mod \phi(n)$. And from the key generation algorithm. $d = d_{r} + r \mod \phi(N)$.

$$e(d_{r} +r) = 1 \mod \phi(N) \\
\implies e e_{r}(d_{r} +r) = e_{r} \mod \phi(N) \\ 
\implies e  e_{r}(e_{r}^{-1} +r) = e_{r} \mod \phi(N) \\
\implies e  (1 +e_{r} r) - e_{r} = 0 \mod \phi(N) \\
\implies e + e_{r}(re - 1) = 0 \mod \phi(N) \\ $$

### Attack
Every parameter on the left side is given, so we can compute $k\phi(N)$ for some $k \in \mathbb{N}$:

$$e + e_{r}(re - 1) = k \phi(N)$$

For RSA, to compute the secret exponent, a multiple of $\phi(N)$ is sufficient to do it. Therefore, we can decrypt the flag.

### IMPLEMENATION
>* [alo_solver.py](https://github.com/msalaani/CTFs/blob/master/Hackfest%207%20-%202023/Finals/Crypto/ALO/alo_solver.py)

```python
#!/usr/bin/env python3

"""
Author : msalaani
Task : ALO - Solver
Event : Hackfest 7 - Finals

"""

from Crypto.Util.number import *

# RSA Key Generation in the YKLM-scheme
# (https://link.springer.com/chapter/10.1007/3-540-45861-1_30

# Attack idea
# https://d-nb.info/972386416/34

N =  ...
e = ...
er = ...
r = ...
c = ...

k_phi = e*(1 + er * r) - er

d_ = inverse(e, k_phi)

print(long_to_bytes(pow(c, d_, N)))
```

> **FLAG:** `HACKFEST{B6902C2ceb244d94aeF6137ED3944BEEd664169bdBf6204d66Cf009D0029863a}`

---
References
* [Sung-Ming Yen, Seungjoo Kim, Seongan Lim, & Sang-Jae Moon. (2003). RSA speedup with chinese remainder theorem immune against hardware fault cryptanalysis.](https://link.springer.com/chapter/10.1007/3-540-45861-1_30)

* [New RSA Vulnerabilities Using Lattice Reduction Methods](https://d-nb.info/972386416/34)
---

# **CRYPTO - FAWDHA**

## **TASK**
#### Points: **500**
#### Solves: **1**
#### Description


> dirou lfawdhaaa
>* [fawdha.sage](https://github.com/msalaani/CTFs/blob/master/Hackfest%207%20-%202023/Finals/Crypto/FAWDHA/fawdha.sage)


```python
#!/usr/bin/env sage

"""

Author : msalaani
Task : Fawdha - Challenge
Event : Hackfest 7 - Finals

"""

from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import random
import hashlib
from Crypto.Util.number import *

try:
	from secret import FLAG
except ImportError:
    FLAG = b"HACKFEST{DuMmy Flag for Dummy .... test}"

class CPRNG:
    def __init__(self,  mod, seed = None, nbits = 512) -> None:
        self.state = seed if seed else random.randint(1, 1 << nbits - 1)
        self.alpha = random.randint(1, 1 << nbits - 1)
        self.beta = random.randint(1, 1 << nbits - 1)
        self.mod = mod
    
    def next(self):
        self.state = self.alpha * self.state * (1 - self.state) + self.beta
        return self.state % self.mod
    
    def __repr__(self) -> str:
        return f"""alpha = {hex(self.alpha)}
beta = {hex(self.beta)}
        """
    
class ECDSA:
    def __init__(self, nbits = 521) -> None:
        p = 0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        self.ec = EllipticCurve(GF(p), (
            0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc,
            0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00
            ))
        self.G = self.ec(
            0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66,
            0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650
            )
        self.n = 0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409
        self.key = random.randint(1, 1 << nbits // 6)
        self.csprng = CPRNG(self.n, self.key)
        
    
    def sign(self, msg):
        h = int.from_bytes(hashlib.sha256(msg).digest(), byteorder = "big")
        k = self.csprng.next()
        r = int((k * self.G).xy()[0])
        s = (inverse(k, self.n) * (h + r * self.key)) % self.n
        return r, s

def encrypt_flag(msg, key):
    key = hashlib.sha256(str(key).encode()).digest()[:16]
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(pad(msg, 16)).hex()


if __name__ == "__main__" :
    ecdsa = ECDSA()
    msg = b"You signed it. Ma3ejbetnich 3aweeeed 3aweeed!"
    ecdsa.sign(msg)
    r, s = ecdsa.sign(msg)

    enc_flag = encrypt_flag(FLAG, ecdsa.key)

    print(ecdsa.csprng)
    print(f"r = {hex(r)}")
    print(f"s = {hex(s)}")
    print(f"{enc_flag = }")

    """
    alpha = 0x6a0bab0492c2ec87298e71bb6fbbefadf20b7692e9dbcec8fbc490122eec1bab37bc8a9feedc8508532d79483bc3d1edefd21d7c490178a1469fd709787d9b2
    beta = 0x1423c84ca7b4735e59910a09b42b8001ecd1d4d5dc7f8fc582012599a1ce5b4b2d69eaf727fc821b54b312596a5f639d9e50a9ba1d9c1d8c2c9f5df83657d167
            
    r = 0x5ce7b426db1b939092097097cd015ab5cdb0ae3620370cab2404b38c33c1e6e21acd5c023087f0160fb768eb6df94337ede12c68ae966355b82d309f8eaa93592e
    s = 0xaea8afbb585e6c03609851b76d013534cf73bdd1274fb88e0f583fb73fa44f676ce54331ce2a611a5728632926d0707719e322c0c34a132554ae9b9767bf4e8ff7
    enc_flag = '8698f8be6cac3e66c96c474dfeb574fd3a318c265ead2f9f49886e77f1933a4e0cdff2ec623ce62f5f4b0ea06a3457637644697c84e6fda1c90b869b4aba5d3da344eb99acba6cef1ef67886bd57d91b'
        
    """
```

## **SOLUTION**
### Challenge
We are given an ECDSA signing script, where it uses a custom random number generator that implements a custom logistic map to generate the nonces. We are given the parameters of the logistic map, a signed message and the encrypted flag.

### Analysis
#### Custom Logistic Map Random Number Generator
The original logistic map is a polynomial mapping of degree 2. It is widely used for the concept of chaos. The original quadratic recurrence equation is:

$$x_0 = {intitial\ value} \\ 
r = {biotic\ potential}, r > 0 \\ 
x_{n+1} =  rx_{n}(1-x_{n}), \forall\ n\in \mathbb{N}^*$$

In this challenge, we used a similar scheme to implement the RNG over $\mathbb{Z}/n\mathbb{Z}$ :
$$x_0 = seed \\
\alpha, \beta \in \mathbb{N},  \\
x_{i+1} =  \alpha x_{i}(1-x_{i}) + \beta \mod n, \forall\ i\in \mathbb{N}^*$$

#### ECDSA second order nonce
The script signed a message twice but we are given only the second output.
Observing the ECDSA class, we can see that the secret key $d$ is used as the seed of the CPRNG to generate the nonces used after in the signature. As its definition says, this is a recursively expressed polynomial. Since the nonces can be expressed using polynomials, we can recover the seed, thus the private key, in polynomial time.

Let's first, express the second order of the CPRNG using the parameters we have.

$$k_0 = d,\\
k_1 = \alpha (k_0) (1 - k_0) + \beta \mod n, \\
k_2 = \alpha (k_1) (1 - k_1) + \beta \mod n \\ $$
The signing equation of $s$ is:
$$(x, y) = k_i \times G \\
r = x \\
s = k_i^{-1}(H(M) + rd) \mod n \\ $$

$G: Generator\ curve\ point$
$k: Nonce$
$H: Hash\ function$

From these equation we can retrieve the the equation of $k_2$ in terms of $d$:

$$k_2 = -\alpha^3s d^4+ 2\alpha^3s\ d^3 \\ - (\alpha^3s - 2\alpha^2\beta s + \alpha^2s)\ d^2 \\ - (2*\alpha^2\beta s - \alpha^2s + r)\ d \\ - \alpha*\beta^2s + \beta s + \alpha*\beta s - h \mod n $$

### Attack

Solving this equation for with the unknown $d$ gives us the secret key.

### IMPLEMENATION
>* [fawdha_solver.sage](https://github.com/msalaani/CTFs/blob/master/Hackfest%207%20-%202023/Finals/Crypto/FAWDHA/fawdh_solver.sage)

```python

#!/usr/bin/env sage

"""

Author : msalaani
Task : FAWDHA - Solver
Event : Hackfest 7 - Finals

"""

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import random
import hashlib
from Crypto.Util.number import *

def decrypt_flag(msg, key):
    key = hashlib.sha256(str(key).encode()).digest()[:16]
    aes = AES.new(key, AES.MODE_ECB)
    return unpad(aes.decrypt(msg), 16)



msg = b"You signed it. Ma3ejbetnich 3aweeeed 3aweeed!"
h = int.from_bytes(hashlib.sha256(msg).digest(), byteorder = "big")

n = ...
alpha = ...
beta = ...
        
r = ...
s = ...
enc_flag = bytes.fromhex('...')



coeffs = [
    -alpha^3*s,
    2*alpha^3*s,
    - (alpha^3*s - 2*alpha^2*beta*s + alpha^2*s),
    - (2*alpha^2*beta*s - alpha^2*s + r),
    - alpha*beta^2*s + beta*s + alpha*beta*s - h
]


bound = 1 << int(521 / 6)
P.<x> = PolynomialRing(Integers(n), "x")
monomials = [x^4, x^3, x^2, x, 1]
f = sum(coeff*monomial for coeff, monomial in zip(coeffs, monomials))
key  = f.roots(multiplicities = False)[0] #f.monic().small_roots(X = bound , epsilon=1/25)[0] # small_roots(f, (bounds,), d = 20, m = 7)[0] # defunds's coppersmith
assert key == 18416832431838432107397
assert decrypt_flag(enc_flag, key) == b"HACKFEST{d31fF31c64f09D1D00240963C56bDCFd685E659D5EfAfd93258D8dB20318a38f}"
```

> **FLAG:** `HACKFEST{d31fF31c64f09D1D00240963C56bDCFd685E659D5EfAfd93258D8dB20318a38f}`

---
References
* [Logistic map](https://en.wikipedia.org/wiki/Logistic_map)
---

# **CRYPTO - LOOK**

## **TASK**
#### Points: **500**
#### Solves: **1**
#### Description


> dell ... <br>
>* [chall.py](https://github.com/msalaani/CTFs/blob/master/Hackfest%207%20-%202023/Finals/Crypto/LOOK/look.py)


```python
#!/usr/bin/env python3

"""

Author : msalaani
Task : Look - Challenge
Event : Hackfest 7 - Finals

"""

from Crypto.Util.number import *
import random

try:
	from secret import FLAG
except ImportError:
    FLAG = b"HACKFEST{DuMmy Flag for Dummy .... test}"

def encrypt(n, P, N, Q = 1):
	if n == 0:
		return 2
	if n == 1:
		return P
	return (P*encrypt(n-1, P, N, Q) - Q*encrypt(n-2, P, N, Q)) % N

if __name__ == "__main__" :
    nbits = 2048
    p, q = [getPrime(nbits >> 2) for _ in '01']
    N = p * q
    e = 3
    Look = encrypt(e, bytes_to_long(FLAG) * (1 << 72) + random.randint(1, 1 << 72), N)
    LookAgain = encrypt(e, bytes_to_long(FLAG) * (1 << 72) + random.randint(1, 1 << 72), N)

    print(f"{N = }")
    print(f"{e = }")
    print(f"{Look = }")
    print(f"{LookAgain = }")

    """
    N = ...
    e = 3
    Look = ...
    LookAgain = ...
    """


```
## **SOLUTION**
### Challenge
This challenge introduces an RSA like encryption scheme using Lucas sequence, known as LUC cryptosystem. The flag is encrypted twice with 2 random and different short paddings.

### Analysis
The challenge is inspired by LUC Cryptosystem but it does not use the right key generation, hoping that won't affect the decryption process (well it does but not in this case ;) ultiple)

#### **Lucas sequence $V_i$**
The Lucas second sequence $\{V_i\}$ is defined by:
$$V_0(P, Q)=2\\
V_1(P, Q)= P\\
V_n(P, Q)= P * V_{n-1}(P, Q) - Q * V_{n-2}(P, Q), \forall n > 1\\
$$

It is proven that that Lucas sequences are recurrent sequences of **polynomials**.

#### **LUC-Like Cryptosystem**
Let's see now how LUC cryptosystem works. This scheme is based on Lucas sequence (described above) and inspires the logic of the RSA cryptosystem.

##### **Key generation**
1. Choose 2 different large primes $p,q$, and calculate the **public modulus** $N=pq$.
2. Calculate the carmichael totient $\Psi(N) = lcm(p\pm 1, q \pm 1)$.
3. Choose a **public exponent** $e$, such that $gcd(S(n), e) = 1$
4. Calculate the **private exponent** $d$ such that $ed = 1 \mod \Psi(n)$

##### **Encryption/Decryption**
To encrypt a message $M$. The ciphertext $C$ is calculated with : $C = V_e(M, 1) \mod N$

To decrypt $C$, M is recovered with: $M = V_d(C, 1) \mod N$

### **Coppersmith's short-pad attack**
Coppersmith theorem, in brief, supposes that, in RSA cryptosystem where <$N,e$> are public key and $N$ is $n$ bit length, encrypting a message $M$ twice such that $M1=2^m M + r_1$ and $M_2 = 2^m M + r_2$, where $r_1$ and $r_2$ are distinct integers with $0 \leq r_1, r_2 < 2^m $ and $m=\lfloor \frac{n}{e^2}\rfloor$, an attacker can recover efficiently $M$ knowning $C_1, C_2$ of $M_1, M_2$ ($r_1$ and $r_2$ are kept unknown).

The attack considers RSA as polynomial $P(X) = X^e - C \mod N$. This can be extended to our used polynomial $V_i$ with $e=3$.


### **Franklin-Reiter related-message attack**
The Franklin-Reiter theorem showed that if two message $M_1$ and $M_2$ such that $M_1 \neq M_2$ and $M_1 = f(M_2) \mod N$ for some linear polynomial $f(x)=ax+b \in \mathbb{Z}_N[x]$ with $b \neq 0$, and given <$N, e, C_1, C_2, f$>, we can recover $M_1, M_2$. This theorem can be extended to higher polynomial degrees under certain restrictions.

### **ATTACK**
Let's now use the two attack to break the scheme. We refer to $V_e$ as polynomial $P$ in $\mathbb{Z}_{N}[X]$.

We have $r_1, r_2$ the paddings used to encrypt the flag, with $m=72$, such that $M_i = 2^m M + r_i$ and $C_i = V_e(M_i, 1)$.

We used the proof of the coppersmith short pad attack to prove ours. Let's define $g_1(x) = V_e(x, 1) - C_1$ and $g_2(x, y) = V_e(x+y, 1) - C_2$. Knowing that when $y = r_2 - r_1$, these polynomials have $M_1$ as a common root: $$g_2(M_1, r_2 - r_1) \\= V_e(M_1 + r_2 - r_1, 1) - C_2 \mod N\\ = V_e(M_2 , 1) - C_2 \mod N \\ = 0 \mod N$$

In other words, $\Delta = r_2 - r_1$ is a root of the "resultant" $h(y) = res_x(g_1, g_2) \in \mathbb{Z}_N[y]$. $\Delta$ is a small root of $h$ modulo $N$ and $|\Delta| < 2^m < N^{1/e^2}$ thus we can solve the polynomial using the lattice reduction technique of Coppermsith. Once $\Delta$ is known, the Franklin-Reiter attack is used used to recover $M_2$ therefore $M$.

### IMPLEMENATION
>* [look_solver.sage](https://github.com/msalaani/CTFs/blob/master/Hackfest%207%20-%202023/Finals/Crypto/LOOK/look_solver.sage)

```python
#!/usr/bin/env sage

"""

Author : msalaani
Task : Look - Solver
Event : Hackfest 7 - Finals

"""
from Crypto.Util.number import *

def CoppersmithShortPadAttack(e,n,C1,C2,pbits, eps=1/25):
	P.<x, y> = PolynomialRing(Zmod(n))
	P2.<y> = PolynomialRing(Zmod(n))

	g1 = (Vi(e, x) - C1).change_ring(P2)
	g2 = (Vi(e, x + y) - C2).change_ring(P2)

	res = g1.resultant(g2, variable=x)

	roots = res.univariate_polynomial().change_ring(Zmod(n)).small_roots(X = 2**pbits, epsilon=eps)
	if len(roots) == 1:
		return int(roots[0])

def FranklinReiterRelatedMessages(C1, C2, N, r, e = 3):
    P.<x> = PolynomialRing(Zmod(N))
    equations = [Vi(e, x) - C1, Vi(e, x+r) - C2]
    g1, g2 = equations
    return int(-composite_gcd(g1, g2).coefficients()[0])

def composite_gcd(g1, g2):
    return g1.monic() if g2 == 0 else composite_gcd(g2, g1 % g2)


def Vi(n, P, N = 1, Q = 1):
	if n == 0:
		return 2
	if n == 1:
		return P
	return (P*Vi(n-1, P, N, Q) - Q*Vi(n-2, P, N, Q))

N = ...
e = 3
C1 = ...
C2 = ...

diff = CoppersmithShortPadAttack(e,N,C1,C2,72)
FLAG = FranklinReiterRelatedMessages(C1, C2, N, diff) >> 72

assert long_to_bytes(FLAG) == b"HACKFEST{425D0544e3813ef357C662e0398A537b9d72a2dbb51D03B9B7B759400decF000}" 

```

> **FLAG:** `HACKFEST{425D0544e3813ef357C662e0398A537b9d72a2dbb51D03B9B7B759400decF000}`

---
References
* [LUC: A New Public Key System](https://cdn.preterhuman.net/texts/cryptology/LUC_PUBL.PDF)
* [Twenty Years of Attacks on the RSA Cryptosystem](https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf)
* [Protocol failures for RSA-like functions using Lucas sequences and elliptic curves](https://link.springer.com/chapter/10.1007/3-540-62494-5_8)
---

# **CRYPTO - ALO REVENGE**

## **TASK**
#### Points: **500**
#### Solves: **0**
#### Description


> ALO ? Ti jeweb 3ad ...
>* [alo_revenge.py](https://github.com/msalaani/CTFs/blob/master/Hackfest%207%20-%202023/Finals/Crypto/ALO_REVENGE/alo_revenge.py)


```python
#!/usr/bin/env python3

"""

Author : msalaani
Task : ALO REVENGE - Challenge
Event : Hackfest 7 - Finals

"""

from Crypto.Util.number import *
from secret import *

nbits = 1024
p, q = [getPrime(nbits) for _  in "01"]

N = p * q
phi = (p - 1) * (q - 1)

while True:
    er = getRandomInteger(nbits // 4)
    r = getRandomInteger(nbits // 4)
    if GCD(er, phi) == 1 :
        dr = inverse(er, phi)
        d = dr + r
        if GCD(d, phi) == 1:
            e = inverse(d, phi)
            break

c = pow(bytes_to_long(flag), e, N)

print(f"{N = }")
print(f"{e = }")
print(f"{c = }")


"""
N = ...
e = ...
c = ...
"""
```
## **SOLUTION**
### Challenge
We are given RSA parameters $(N, e)$ and the RSA encrypted flag. Other parameters $(e_{r}, r)$ from **YKLM** key generation are kept secret. This is the revenge version of the ALO task seen above.

### Analysis
This challenge introduces the same *YKLM* scheme shown earlier but without giving $(e_{r}, r)$. From key generation we can see that $e$ satisfies an equation $ex + y = 0 \mod \phi(N)$ with $x=1+e_rr$ and $y = -e_r$. We can see we have a weird conditions for key generation:
$x \leq \frac{1}{3}N^{\frac{1}{4}} \ \ and \ \  |y| \leq \frac{1}{2}cN^{\frac{1}{4}}$. This can be used to factor $N$ in time polynomial in $\log(N)$.

### Attack
This challenge attack is the implementation of the **Generalized Wiener Attack** from 
[A Generalized Wiener Attack on RSA](https://iacr.org/archive/pkc2004/29470001/29470001.pdf) paper.

Briefly, the paper prooves that, in RSA context with (N, e) public key tuple such that $N=pq$ and $p-q \leq cN^{\frac{1}{2}}$, if $e$ satifies the equation $ex+y=0 \mod \phi(N)$ with 
$$x \leq \frac{1}{3}N^{\frac{1}{4}},\ |y| \leq \frac{1}{2}cN^{-\frac{3}{4}}ex\ \ and\ \ c \leq1$$
then $N$ can be factored in polynomial time. (**Theorem 2**)

### IMPLEMENATION
>* [alo_revenge_solver.sage](https://github.com/msalaani/CTFs/blob/master/Hackfest%207%20-%202023/Finals/Crypto/ALO_REVENGE/alo_revenge_solver.sage)

```python
#!/usr/bin/env python3

"""
Author : msalaani
Task : ALO REVENGE - Solver
Event : Hackfest 7 - Finals

"""

from Crypto.Util.number import long_to_bytes
from sage.all import *

def GeneralizedWienerAttack_1(e, N):
    
    # https://iacr.org/archive/pkc2004/29470001/29470001.pdf

    # 1. Compute continued fractions e / N
    convergents = continued_fraction(ZZ(e) / N).convergents()
    for convergent in convergents:
        k = convergent.numerator()
        x = convergent.denominator()
        if (k != 0):
            # 2.a Compute s, t and p_tild
            s = N + 1 - e*x // k # ~= p + q
            t = s**2 - 4*N # ~= p - q
            if t >= 0:
                if Integer.is_square(t):
                    t = isqrt(t)
                    if (s+t) & 1 == 0:
                        p_tild = (s+t) // 2 # ~= p
                        if N % p_tild == 0 and (1 < p_tild < N): # Direct Solution
                            return int(p_tild), int(N // p_tild)

                        else: # Coppersmith
                            # 2.b apply coppersmith 
                            x_ = PolynomialRing(Zmod(N), "x").gen()
                            B = isqrt(isqrt(N)) # N ^ 1/4
                            f = p_tild + x_
                            for k_ in range(-3, 3):
                                fc = f + (2*k_+1) * B 
                                roots = fc.small_roots(X = B, epsilon = 1/25)
                                if len(roots) != 0:
                                    for p_r in roots:
                                        if N % p_r == 0:
                                            return int(p_r), int(N // p_r)
    return None, None

N = ...
e = ...
c = ...
    
p, q = GeneralizedWienerAttack_1(e, N)
if p and q:
    d = inverse_mod(e, (p-1)*(q-1))
    FLAG = int(pow(c, d, N))

    assert long_to_bytes(FLAG) == b"HACKFEST{2fb8eA6a8BA564276a581a5B51032D5331a7B953C4d2b864a65c2D96Ae9e1947}"


```

> **FLAG:** `HACKFEST{2fb8eA6a8BA564276a581a5B51032D5331a7B953C4d2b864a65c2D96Ae9e1947}`

---
References
* [A Generalized Wiener Attack on RSA](https://iacr.org/archive/pkc2004/29470001/29470001.pdf) 
---
