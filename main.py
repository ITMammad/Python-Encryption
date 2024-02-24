# In The Name Of Allah
# Developed With <3 By ITMammad...
# website: https://itmammad.ir

import hashlib

class Encryption:
    def __init__(self, key):
        self.key = hashlib.sha256(("Key is: " + (key*2)).encode()).digest()
        key_blocks = []

        for i in range(8):
            k = (self.key[i] ^ self.key[i+1]) * (self.key[i+2] ^ self.key[i+3])
            while k > 255:
                k = k // 4
                
            key_blocks.append(k)

        self.key_blocks = key_blocks

    def encrypt(self, data):
        data_bytes = [ord(x) for x in str(data)]
        data_blocks = []

        for i in range(0, (len(data_bytes) // 4) * 4, 4):
            data_blocks.append([data_bytes[i], data_bytes[i+1], data_bytes[i+2], data_bytes[i+3]])
        
        match len(data_bytes) % 4:
            case 0:
                pass

            case 1:
                data_blocks.append(data_bytes[-1:])

            case 2:
                data_blocks.append(data_bytes[-2:])

            case 3:
                data_blocks.append(data_bytes[-3:])

        cipher_bytes = []
        for i in range(len(data_blocks)):
            data_block = data_blocks[i]
            key_byte = self.key_blocks[i % 8]

            for b in data_block:
                cipher_bytes.append(b ^ key_byte)

        return "".join([hex(x).replace("0x", "") if len(str(hex(x).replace("0x", ""))) == 2 else "0"+hex(x).replace("0x", "") for x in cipher_bytes])

    def decrypt(self, data):
        cipher_bytes = bytes.fromhex(data)
        cipher_blocks = []

        for i in range(0, (len(cipher_bytes) // 4) * 4, 4):
            cipher_blocks.append([cipher_bytes[i], cipher_bytes[i+1], cipher_bytes[i+2], cipher_bytes[i+3]])
        
        match len(cipher_bytes) % 4:
            case 0:
                pass

            case 1:
                cipher_blocks.append(cipher_bytes[-1:])

            case 2:
                cipher_blocks.append(cipher_bytes[-2:])

            case 3:
                cipher_blocks.append(cipher_bytes[-3:])

        data_bytes = []
        for i in range(len(cipher_blocks)):
            data_block = cipher_blocks[i]
            key_byte = self.key_blocks[i % 8]

            for b in data_block:
                data_bytes.append(b ^ key_byte)
            
        return "".join([chr(x) for x in data_bytes])

op = ""
while not op in ["E", "D", "e", "d"]:
    op = input("Enter Operation (Encryption/Decryption): (E/D/e/d)? ")

dictionary = { "adverb": "", "verb": "" }
if op in ["E", "e"]:
    dictionary["adverb"] = "Encryption"
    dictionary["verb"] = "Encrypt"
else:
    dictionary["adverb"] = "Decryption"
    dictionary["verb"] = "Decrypt"

key = input(f"Enter {dictionary['adverb']} Password/Key: ")
data = input(f"Enter Data That You Want To {dictionary['verb']}: ")

encryption = Encryption(key)
if op in ["E", "e"]:
    print(encryption.encrypt(data))
else:
    print(encryption.decrypt(data))