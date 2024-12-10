from Crypto.Cipher import DES

# Key must be 8 bytes
key = b'abcdefgh'  
cipher = DES.new(key, DES.MODE_ECB)

# Plaintext must be a multiple of 8 bytes
plaintext = b'HELLO123WWWWWWWW'
ciphertext = cipher.encrypt(plaintext)

print("Ciphertext:", ciphertext.hex())

# Decrypting
decrypted = cipher.decrypt(ciphertext)
print("Decrypted:", decrypted.decode())
