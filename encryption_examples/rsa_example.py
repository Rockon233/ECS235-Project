from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

# Key generation
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

print("Private Key:")
print(private_key.decode())
print("\nPublic Key:")
print(public_key.decode())

# Encryption
plaintext = b'Hello RSA!'
cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
ciphertext = cipher.encrypt(plaintext)
print("\nCiphertext (hex):", ciphertext.hex())

# Decryption
cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
decrypted = cipher.decrypt(ciphertext)
print("\nDecrypted Plaintext:", decrypted.decode())
