from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Key must be 16, 24, or 32 bytes for AES
key = b'sixteen_byte_key'  # 16-byte key, Byte string
cipher = AES.new(key, AES.MODE_ECB)

# Plaintext (must be padded to be a multiple of 16 bytes)
plaintext = b'HELLO AES!'
padded_plaintext = pad(plaintext, 16)  # Pad to match block size
ciphertext = cipher.encrypt(padded_plaintext)

print("Ciphertext (hex):", ciphertext.hex())

# Decrypting
decrypted_padded = cipher.decrypt(ciphertext)
decrypted_plaintext = unpad(decrypted_padded, 16)
print("Decrypted:", decrypted_plaintext.decode())
