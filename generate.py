from Crypto.PublicKey import RSA

key = RSA.generate(2048)
encrypted_key = key.export_key()

file_out = open("private.pem", "wb")
file_out.write(encrypted_key)
file_out.close()

print(key.publickey().export_key())
