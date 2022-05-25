from sympy import Matrix
from secret import flag, key

class Hill:
	def __init__(self,m = 3, key = None, alphabet_pool = "abcdefghijklmnopqrstuvwxyz"):
		self.m = m
		self.N = len(alphabet_pool)
		self.alphabet, self.reverse_alphabet = self.__genAlpha(alphabet_pool)
		
		if key != None:	
			self.key = self.__getKey(key)
			try:
				self.inv_key = self.key.inv_mod(self.N)
			except:
				self.inv_key = None
				pass

	def __genAlpha(self, alphabet_pool = "abcdefghijklmnopqrstuvwxyz"):
		alphabet, reverse_alphabet = {}, {}
		
		for character in alphabet_pool:
			key, value = character, alphabet_pool.index(character)
			alphabet[key] = value
			reverse_alphabet[value] = key

		return alphabet, reverse_alphabet

	def __getKey(self, key):
		if isinstance(key, str):
			return self.__t2m(key, (self.m, self.m))
		elif isinstance(key, list):
			return Matrix(key)
		elif isinstance(key, Matrix):
			return key
		else:
			raise ValueError('Key must be String, List Matix or Matrix')
		
	def __pad(self, text):		
		return text + self.reverse_alphabet[self.N-1] * ((self.m - len(text))%self.m )

	def __t2m(self, text, shape):
		assert len(text) == shape[0] * shape[1]
		
		text_mat = [self.alphabet[char] for char in text]
		text_mat = Matrix(text_mat)
		text_mat = text_mat.reshape(shape[0], shape[1])

		return text_mat

	def __m2t(self, mat, shape):
		assert mat.shape == shape
		
		text = mat.reshape(1, shape[0] * shape[1])
		text = "".join([self.reverse_alphabet[n] for n in text])
		
		return text

	def __encrypt(self, vtext, mat_key):
		return mat_key * vtext %self.N
	
	def encrypt(self, text):
		if len(text) %self.m != 0:
			text = self.__pad(text)
		
		rows, cols = len(text) // self.m, self.m
		text = self.__t2m(text, (rows, cols))
		cipher = ""
		for i in range(text.rows):
			c = self.__encrypt(text.row(i).transpose(), self.key)
			cipher += self.__m2t(c, (self.m, 1))
		
		return cipher
	
	def decrypt(self, cipher):
		assert len(cipher) %self.m == 0, "Ciphertext is no padded."
		assert self.inv_key != None, "Cannot decrypt with this key value."
		
		rows, cols = len(cipher) // self.m, self.m
		cipher = self.__t2m(cipher, (rows, cols))
		ciphertext = ""
		for i in range(cipher.rows):
			c = self.__encrypt(cipher.row(i).transpose(), self.inv_key)
			ciphertext += self.__m2t(c, (self.m, 1))
		
		return ciphertext

	def __repr__(self) -> str:
		repr = "Hill Cipher "
		repr += str(hash(self))
		repr += "\n" + f"Key size: {(self.m, self.m)}"

		if self.key:
			repr += "\n" + f"Key : {self.key}"

		repr += "\n" + f"Modulus: {self.N}"
		repr += "\n" + f"Alphabet: " + str("".join(self.alphabet.keys()))

		return repr + "\n"

if __name__ == "__main__":

	alphabet = "{}abcdefghijklmnopqrstuvwxyz_"
	cipher = Hill(key = key, alphabet_pool= alphabet)
	flag_enc = cipher.encrypt(flag)
	print(flag_enc)
	
	# bbcbp_zqrafjq}ehowmdw{jifop_y_wo_hqoaoetavcicwdadgoafkatlkuf

