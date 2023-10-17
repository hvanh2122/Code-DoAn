from base64 import b64encode, b64decode
from utils.converter import *

class AESBase:
    def __init__(self, rounds, order):
        self.ROUND = rounds
        self.ORDER = order
        self.ROUND_KEY = []
        self.S_BOX = []
        self.INV_S_BOX = []

    def add_round_key(self, key_str):
        pass

    def convert_round_key(self):
        self.ROUND_KEY = np.concatenate(self.ROUND_KEY)
        temp = []
        for i in range(self.ROUND + 1):
            temp.append(self.ROUND_KEY[i * 4:i * 4 + 4])
        self.ROUND_KEY = temp

    def encrypt_process(self, message):
        hex_data = key_to_hex_array(message)
        cipher_arr = add_round_key(hex_data, self.ROUND_KEY[0])
        for i in range(1, self.ROUND + 1):
            arr = cipher_arr
            index = i % self.ORDER - 1
            arr = sub_bytes(arr, self.S_BOX[index], self.INV_S_BOX[index])
            arr = shift_row(arr)
            if i != self.ROUND:
                arr = mix_column(arr)
            arr = add_round_key(arr, self.ROUND_KEY[i])
            cipher_arr = arr
        return cipher_arr

    def decrypt_process(self, cipher_hex):
        hex_data = hex_to_matrix(cipher_hex)
        plain_arr = add_round_key(hex_data, self.ROUND_KEY[-1])
        for i in range(self.ROUND - 1, -1, -1):
            arr = plain_arr
            arr = shift_row(arr, left=False)
            arr = sub_bytes(arr, self.S_BOX[i % self.ORDER], self.INV_S_BOX[i % self.ORDER], inverse=True)
            arr = add_round_key(arr, self.ROUND_KEY[i])
            if i != 0:
                arr = inverse_mix_column(arr)
            plain_arr = arr

        return plain_arr

    def encrypt(self, key_str, message, type='hex'):
        text_array = add_padding(message)
        self.add_round_key(key_str)
        hex_encrypt = ''
        for i in text_array:
            cipher_matrix = self.encrypt_process(i)
            cipher_text = list(np.array(cipher_matrix).reshape(-1,))
            for j in cipher_text:
                hex_encrypt += f'{j:02x}'
        self.ROUND_KEY = []
        if type == 'b64':
            return b64encode(bytes.fromhex(hex_encrypt)).decode()
        if type == '0b':
            return f'{int(hex_encrypt, 16):0>b}'
        if type == '__all__':
            return {
                'hex': hex_encrypt,
                'b64': b64encode(bytes.fromhex(hex_encrypt)).decode(),
                '0b': bin(int(hex_encrypt, 16))[2:].zfill(len(hex_encrypt) * 4)
            }
        return hex_encrypt

    def decrypt(self, key_str, cipher, type='hex'):
        if type in ['hex', '0b', 'b64']:
            self.add_round_key(key_str)
            data = ''
            if type == 'b64':
                cipher = b64decode(cipher).hex()
            elif type == '0b':
                cipher = hex(int(cipher, 2)).replace('0x', '')
            if len(cipher) % 32 == 0 and len(cipher) > 0:
                examine = cipher
                while len(examine) != 0:
                    plain_matrix = self.decrypt_process(examine[:32])
                    plain_arr = list(np.array(plain_matrix).reshape(-1,))
                    plain_arr = del_padding(plain_arr)
                    for j in plain_arr:
                        data += chr(j)
                    if len(examine) == 32:
                        examine = ''
                    else:
                        examine = examine[32:]
                self.ROUND_KEY = []
                return data
            else:
                raise Exception(f"Hex: {cipher}, should be non-empty multiple of 32bits")
        else:
            raise Exception(f"type := ['hex', '0b', 'b64'] but got '{type}'")