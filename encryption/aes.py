from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESOBJ:
    @staticmethod
    def encryption(key, plaintext):
        if len(key) not in (16, 24, 32):
            raise ValueError("Key length must be 16, 24 or 32 bytes")
        # Convert plaintext to bytes
        plaintext = plaintext.encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)
        # Pad to match block size
        padded_plaintext = pad(plaintext, 16) 
        ciphertext = cipher.encrypt(padded_plaintext)
        return ciphertext
    
    @staticmethod
    def decryption(key, ciphertext):
        if len(key) not in (16, 24, 32):
            raise ValueError("Key length must be 16, 24 or 32 bytes")
        # Create a new AES cipher object with the given key and ECB mode
        cipher = AES.new(key, AES.MODE_ECB)
        
        decrypted_padded = cipher.decrypt(ciphertext)
        decrypted_plaintext = unpad(decrypted_padded, 16)
        return decrypted_plaintext


if __name__ == "__main__":
    key = b'sixteen byte key'
    plaintext = 'HELLO AES!'
    ciphertext = AESOBJ.encryption(key, plaintext)
    decrypted = AESOBJ.decryption(key, ciphertext)
    
    print(f"Plaintext is: {plaintext}")
    print(f"Ciphertext is: {ciphertext}")
    print(f"Decryptedtext is: {decrypted.decode()}")

    assert plaintext == decrypted.decode()
    print("Test Passed!")