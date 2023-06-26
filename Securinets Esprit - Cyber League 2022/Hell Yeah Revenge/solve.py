from sympy import Matrix
from sympy.matrices.common import NonInvertibleMatrixError, NonSquareMatrixError
from chall import Hill

class Hill_KnownPlaintextAttack:
	def __init__(self, ct, kpt, m, alphabet_pool = "abcdefghijklmnopqrstuvwxyz"):
		self.m = m
		self.shape = (m, m)
		self.N = len(alphabet_pool)
		self.kpt = kpt
		self.ct = ct
		self.alphabet, self.reverse_alphabet = self.__genAlpha(alphabet_pool)

		assert len(self.ct) == len(self.kpt)
		assert len(self.kpt) %self.m**2 == 0
	
	def __genAlpha(self, alphabet_pool = "abcdefghijklmnopqrstuvwxyz"):
		alphabet, reverse_alphabet = {}, {}
		
		for character in alphabet_pool:
			key, value = character, alphabet_pool.index(character)
			alphabet[key] = value
			reverse_alphabet[value] = key

		return alphabet, reverse_alphabet

	def __t2m(self, text, shape):
		assert len(text) == shape[0] * shape[1]
		
		text_mat = [self.alphabet[char] for char in text]
		text_mat = Matrix(text_mat)
		text_mat = text_mat.reshape(shape[0], shape[1])

		return text_mat
	
	def KPA(self):
		try:
			kpt = self.__t2m(self.kpt, (self.m, self.m))
			kpt = kpt.inv_mod(self.N)
		except NonInvertibleMatrixError:
			print("Known plaintext attack is not possible")
			return
		except NonSquareMatrixError:
			return
		ct = self.__t2m(self.ct, (self.m, self.m))
		return (kpt*ct %self.N).transpose()


alphabet = "{}abcdefghijklmnopqrstuvwxyz_"
attack = Hill_KnownPlaintextAttack("bbcbp_zqr", "securinet", 3, alphabet_pool=alphabet)
key = attack.KPA()
print(key)
cipher = Hill(key = key,alphabet_pool=alphabet)

print(cipher.decrypt("bbcbp_zqrafjq}ehowmdw{jifop_y_wo_hqoaoetavcicwdadgoafkatlkuf"))
