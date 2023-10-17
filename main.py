import time
from models.AES128 import *
from models.AES192 import *
from models.AES256 import *

if __name__ == '__main__':
    aes128 = AES128()
    aes192 = AES192()
    aes256 = AES256()

    key128 = 'The cryptography'
    key192 = 'Cryptographic algorithms'
    key256 = 'Select an irreducible polynomial'
    msg = 'generate dynamic key dependent S-Box'
    encode = '__all__'  # hex, b64 => base64, 0b => binary

    # 128 bit
    start = time.time()
    x = aes128.encrypt(key128, msg, encode)
    print(f"AES-128 Encrypted:\n\t hex: {x['hex']}\n\t b64: {x['b64']}\n\t bin: {x['0b']}")
    finish = time.time()
    duration = finish - start
    print("\t\tAES-128 Encryption speed: {:.2f} Kbits/seconds".format(250000 / duration))

    # decode from hex (default)
    start = time.time()
    z = aes128.decrypt(key128, x['hex'])
    finish = time.time()
    duration = finish - start
    print("\nAES-128 Decrypted (from hex): {} \t Speed: {:.2f} Kbits/seconds".format(z, 250000 / duration))

    start = time.time()
    z = aes128.decrypt(key128, x['b64'], 'b64')
    finish = time.time()
    duration = finish - start
    print("\nAES-128 Decrypted (from base64): {} \t Speed: {:.2f} Kbits/seconds".format(z, 250000 / duration))

    start = time.time()
    z = aes128.decrypt(key128, x['0b'], '0b')
    finish = time.time()
    duration = finish - start
    print("\nAES-128 Decrypted (from bin): {} \t Speed: {:.2f} Kbits/seconds".format(z, 250000 / duration))

    # 192 bit
    start = time.time()
    x = aes192.encrypt(key192, msg, encode)
    print(f"AES-192 Encrypted:\n\t hex: {x['hex']}\n\t b64: {x['b64']}\n\t bin: {x['0b']}")
    finish = time.time()
    duration = finish - start
    print("\t\tAES-192 Encryption speed: {:.2f} Kbits/seconds".format(250000 / duration))

    #decode from hex (default)
    start = time.time()
    z = aes192.decrypt(key192, x['hex'])
    finish = time.time()
    duration = finish - start
    print("\nAES-192 Decrypted (from hex): {} \t Speed: {:.2f} Kbits/seconds".format(z, 250000 / duration))

    start = time.time()
    z = aes192.decrypt(key192, x['b64'], 'b64')
    finish = time.time()
    duration = finish - start
    print("\nAES-192 Decrypted (from base64): {} \t Speed: {:.2f} Kbits/seconds".format(z, 250000 / duration))

    start = time.time()
    z = aes192.decrypt(key192, x['0b'], '0b')
    finish = time.time()
    duration = finish - start
    print("\nAES-192 Decrypted (from bin): {} \t Speed: {:.2f} Kbits/seconds".format(z, 250000 / duration))

    #256 bit
    start = time.time()
    x = aes256.encrypt(key256, msg, encode)
    print(f"AES-256 Encrypted:\n\t hex: {x['hex']}\n\t b64: {x['b64']}\n\t bin: {x['0b']}")
    finish = time.time()
    duration = finish - start
    print("\t\tAES-256 Encryption speed: {:.2f} Kbits/seconds".format(250000 / duration))

    #decode from hex (default)
    start = time.time()
    z = aes256.decrypt(key256, x['hex'])
    finish = time.time()
    duration = finish - start
    print("\nAES-256 Decrypted (from hex): {} \t Speed: {:.2f} Kbits/seconds".format(z, 250000 / duration))

    start = time.time()
    z = aes256.decrypt(key256, x['b64'], 'b64')
    finish = time.time()
    duration = finish - start
    print("\nAES-256 Decrypted (from base64): {} \t Speed: {:.2f} Kbits/seconds".format(z, 250000 / duration))

    start = time.time()
    z = aes256.decrypt(key256, x['0b'], '0b')
    finish = time.time()
    duration = finish - start
    print("\nAES-256 Decrypted (from bin): {} \t Speed: {:.2f} Kbits/seconds".format(z, 250000 / duration))
