from passlib.context import CryptContext

# Create an instance of CryptContext with the "bcrypt" hashing scheme
pwd_cxt = CryptContext(schemes="bcrypt", deprecated="auto")
class Hash():
	def bcrypt(password: str):
		return pwd_cxt.hash(password)

# Verify a plain password against a hashed password
	def verify_password(hashed_password, plain_password):
		return pwd_cxt.verify(plain_password, hashed_password)