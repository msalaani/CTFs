from Crypto.Util.number import *
from secret import flag

nbit = 2048
pbit = 32
mult = 8
flag = bytes_to_long(flag)

def genkey(nbit, pbit, mult=1):
	e = 0x10001
	n = 1
	while n.bit_length() < nbit:
		p = getPrime(pbit)
		r = getRandomRange(1, mult + 1)
		if (n * p**r).bit_length() <= nbit + pbit and GCD(e, p-1) == 1:
			n *= p**r
	return n, e

n, e = genkey(nbit, pbit, mult)
c = pow(flag, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{c = }")

"""
n = 1572635982452809645423819690563485217328428865657188045786125894618667627108430176723573709631092150403603957486057259109577782279870163440283817658166049754425107266296212365655343753685737483045424411958309199134996343899446948094057166272021080361597594670326399899385067383361870595495161098741683967159370807806861213608136883316400929452887073879444758493008651788463619549537351669166651191393736358107851787145025143410979104429441972119798423091707335304680530242381925868515299457522069426996620186792408188100871682068710069868296511654740486722055835602049483785661130522119397996862072996010353039189401861233997
e = 65537
c = 1419117076907524987883708061013382541177206687421719889124893097541155759357177972941280026820515666869374693906889325528756603806812249114806465675996639965533644918093577336593516267962929141484653827325133280790994674468473816971690473352874904780192339174440208336856868160151578325758843788760787602894739027749115274167089123215921326378331464317778123081310510137171579292489537314047065978500260997076069333250485333023260426332255328994247132807361370194464129514519010255583389099571682237992708344130532544204601752053488369128392608203133269261187855718348075304651468332939336785294283482439134476864432521566089
"""