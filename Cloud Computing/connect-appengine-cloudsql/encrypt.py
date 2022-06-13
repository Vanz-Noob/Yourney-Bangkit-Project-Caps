from passlib.hash import sha256_crypt

password = sha256_crypt.encrypt("re")
password2 = sha256_crypt.encrypt("tono")

print(password)
print(password2)

print(sha256_crypt.verify("re", password))