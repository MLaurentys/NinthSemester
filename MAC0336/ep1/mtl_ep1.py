from sage.all import *

import binascii
import codecs
import sys
import hashlib

from os import urandom
import os
import codecs

def generate_file(doc, initial_string, r_str):
    file = doc
    nusp = initial_string
    if os.path.exists(file): os.remove(file)
    os.mknod(file)
    f = open(file, 'a')
    f.write(nusp)
    f.close()
    f = open(file, 'ab')
    f.write(r_str)
    f.close()

# 160-bit public keys ---> (512 - 160)bits of padding
PUBLIC_PRIME_ALICE = 1041336674237055084071818376299951482429526594679
PUBLIC_GENERATOR_ALICE = 13
PRIVATE_KEY_ALICE = 190

PUBLIC_PRIME_BETO  = 745716481705128370884830807039213906473905739187
PUBLIC_GENERATOR_BETO  = 2
PRIVATE_KEY_BETO  = 911

KEM_PRIME = 1041336674237055084071818376299951482429526594679
KEM_GENERATOR = 13
KEM_PVT_ALICE = 800
KEM_PVT_BETO  = 1000

class ElGamal_Generator:

    def __init__(self, prime, generator, pvt_key):
        self.field = Integers (prime, is_field=True)
        #verifies that 'prime' is indeed prime
        self.field.is_field (proof=True)
        # checks 'generator' is indeed a generator
        if generator not in self.field.unit_gens():
            raise ValueError("Not a generator of the field")
        self.prime = prime
        self.generator = generator
        self._pvt_key = pvt_key
        self.T = power_mod (generator, pvt_key, prime)
        self.chosen_k = set()

    def get_public_info (self):
        return (self.prime, self.generator, self.T)

    def _get_all_info(self):
        return (self.prime, self.generator, self._pvt_key, self.T)

    def sign(self, message):
        mes = int(message,16)
        y = -1
        z = -1
        while (True):
            while (True):
                k = self.field.random_element()
                if k not in self.chosen_k:
                    self.chosen_k.add(k)
                    break
            if (gcd (k.lift(), self.prime - 1) == 1):
                k_inv = inverse_mod (k.lift(), self.prime - 1)
                y = power_mod (self.generator, k.lift(), self.prime)
                z = ((mes - self._pvt_key*y) * k_inv) % (self.prime - 1)
                break
        return (y, z)

class ElGamal_Verifier:

    def verify_signature (self, pub_info, signature, message, verb=False):
        info = pub_info
        f = power_mod (info[1], int(message,16), info[0])
        s = (power_mod (info[2], signature[0], info[0]) *\
            power_mod (signature[0], signature[1], info[0])) % info[0]
        if(verb):
            print("Left side  = " + str(f))
            print("Right side = " + str(s))
        if f == s:
            return True
        return False

class KEM_user():
    def __init__(self, prime, generator, pvt_key):
        self.field = Integers (prime, is_field=True)
        #verifies that 'prime' is indeed prime
        self.field.is_field (proof=True)
        # checks 'generator' is indeed a generator
        if generator not in self.field.unit_gens():
            raise ValueError("Not a generator of the field")
        self.prime = prime
        self.generator = generator
        self._pvt_key = pvt_key
        self.T = power_mod (generator, pvt_key, prime)
        self.chosen_k = set()

    def get_u(self):
        while (True):
            k = self.field.random_element()
            if k not in self.chosen_k and k != self.prime-1:
                self.chosen_k.add(k)
                break
        k = k.lift()
        u = power_mod (self.generator, k, self.prime)
        return (k,u)
    
    def get_t(self): return self.T

def get_binary_representation_512_bits_of_hex(h):
    bin_h = bin(int(h, 16))[2:]  # [2:] Tira o 0b da frente
    bin_h_512bits = '0' * (512 - len(bin_h)) + bin_h

    return bin_h_512bits

def hamming_distance(b1, b2):
    distance = 0
    for x1, x2 in zip(b1, b2):
        if x1 != x2:
            distance += 1
    return distance

def hamming_distance_with_hex_strings(h1, h2):
    bin_h1 = get_binary_representation_512_bits_of_hex(h1)
    bin_h2 = get_binary_representation_512_bits_of_hex(h2)

    distance = 0
    for x1, x2 in zip(bin_h1, bin_h2):
        if x1 != x2:
            distance += 1
    return distance


def sha512_file(filepath):
    BLOCK_SIZE = 65536  # = 64Kb

    file_hash = hashlib.sha512()
    with open(filepath, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)

    return file_hash.hexdigest()


# Generate documents and print their basic information
def gen_docs(docss):
    docs = docss
    nusps = ['9793714', '9793715']
    r_str = urandom(10**5) #100kB of random bytes
    sha512_hashs = [-1,-1]
    for ind in [0,1]:
        print('\nFile: %s' % docs[ind])
        generate_file(docs[ind], nusps[ind], r_str)
        print("First 100 bytes in hex encoding:")
        f = open(docs[ind], 'r')
        byts = binascii.hexlify(f.read(100))
        print(byts)
        f.close()
        sha512_hashs[ind] = sha512_file(docs[ind])
        print('SHA512 hash:')
        print(int(sha512_hashs[ind], 16))
    return sha512_hashs
# Creates ElGamal encrypter and prints info
def gen_generator(p,g,S,name):
    gen = ElGamal_Generator(p,g,S)
    k = gen._get_all_info()
    print("\n%s\'s keys is:" % name)
    print("p = " + str(k[0]))
    print("g = " + str(k[1]))
    print("S = " + str(k[2]))
    print("T = " + str(k[3]))
    return gen
# Makes encrypter encrypt message
def sign_message(encrypter, message, enc_n, mes_n):
    aux = encrypter.sign(message)
    print('\n%s\'s signature of %s is:' % (enc_n, mes_n))
    print("y = %s\nz = %s" % (("%x" % aux[0]), ("%x" % aux[1])))
    ali_signature = (aux[0], aux[1], ("%x" % aux[0]) + ("%x" % aux[1]))
    print('Resulting in:')
    print(ali_signature[2])
    return ali_signature
# Verifies validity of encryption
def verify_sig(pub_info, signature, message, sign_n, mes_n):
    verifier = ElGamal_Verifier()
    print("Verifying if %s is valid for %s" % (sign_n, mes_n))
    ret = verifier.verify_signature(pub_info, signature, message, verb=True)
    print(ret)
    return ret
# Follows exercise 9 prompt
def exer_9(alice):
    with open('arq1.txt', 'rw') as f:
        contentA = f.read()
        aux = list(contentA)
        aux[0] = 'Y' if aux[0] != 'Y' else 'Z'
        contentB = ''.join(aux)
        hashAux = hashlib.sha512(contentB).hexdigest()
    hashA = sha512_file('arq1.txt')
    assinaturaHashA = alice.sign(hashA)
    assinaturaHashAux = alice.sign(hashAux)
    print("\nFile arq1.txt")
    print("hashA = %s" % hashA)
    print('assinaturaHashA:')
    print("y = %s\nz = %s" % (("%x" % assinaturaHashA[0]), ("%x" % assinaturaHashA[1])))
    print("\nFile EDITED arq1.txt")
    print("hashAux = %s" % hashAux)
    print('assinaturaHashAux:')
    print("y = %s\nz = %s" % (("%x" % assinaturaHashAux[0]), ("%x" % assinaturaHashAux[1])))
    print("\nHamming distance between both signatures: %s" % \
        hamming_distance_with_hex_strings(("%x" % assinaturaHashA[0]) + ("%x" % assinaturaHashA[1]), ("%x" % assinaturaHashAux[0]) + ("%x" % assinaturaHashAux[1])))
    return ("%x" % assinaturaHashA[0]) + ("%x" % assinaturaHashA[1])

# Follows exercise 10 prompt
def exer_10(assinaturaHashA, beto):
    if os.path.exists('arq2.txt'): os.remove('arq2.txt')
    with open('arq1.txt', 'r') as f:
        txt = f.read()
    os.mknod('arq2.txt')
    with open('arq2.txt', 'a') as f:
        f.write(txt)
        f.write(assinaturaHashA)
    with open('arq2.txt', 'r') as f:
        txt = f.read()
    hashB = sha512_file('arq2.txt')
    assinaturaHashB = beto.sign(hashB)
    print("\nHash of arq2.txt:")
    print(hashB)
    print("Assinatura do Beto sobre arq2.txt:")
    print("y = %s\nz = %s" % (("%x" % assinaturaHashB[0]), ("%x" % assinaturaHashB[1])))
    verify_sig(beto.get_public_info(), assinaturaHashB, hashB, "assinaturaHashB", "hash of arq2.txt")

# Follows exercises 11 and 12 prompt
def exer_11_12():
    alice = KEM_user(KEM_PRIME, KEM_GENERATOR, KEM_PVT_ALICE)
    beto = KEM_user(KEM_PRIME, KEM_GENERATOR, KEM_PVT_BETO)
    (r_a, u_a) = alice.get_u()
    (r_b, u_b) = beto.get_u()
    K_a = "%x" % (power_mod(u_b, KEM_PVT_ALICE, KEM_PRIME) * power_mod(beto.get_t(), r_a, KEM_PRIME))
    K_b = "%x" % (power_mod(u_a, KEM_PVT_BETO, KEM_PRIME) * power_mod(alice.get_t(), r_b, KEM_PRIME))
    print("Ka = %s\nKb = %s" % (K_a, K_b))
    print("Hamming distance:\n%s"% hamming_distance_with_hex_strings(K_a, K_b))

def main():
    if len(sys.argv) != 1:
        print("Usage: No arguments (just make sure arq1.txt exists)")
        sys.exit(0)

    docs = ['documento1', 'documento2']

    print("---\nGenerating documents\n---")
    hashs = gen_docs(docs)

    print("---\nGenerating encrypters\n---")
    eg_gen_alice = gen_generator(PUBLIC_PRIME_ALICE, PUBLIC_GENERATOR_ALICE, PRIVATE_KEY_ALICE, "Alice")
    eg_gen_beto = gen_generator(PUBLIC_PRIME_BETO, PUBLIC_GENERATOR_BETO, PRIVATE_KEY_BETO, "Beto")

    print("---\nSigning hashes\n---")
    ali_signatures = [sign_message(eg_gen_alice, hashs[0], "Alice", docs[0]),
                      sign_message(eg_gen_alice, hashs[1], "Alice", docs[1])]
    

    print('---\nHamming distance between signatures is:\n---')
    print(hamming_distance_with_hex_strings(ali_signatures[0][2], ali_signatures[1][2]))

    print("---\nVerifying signatures\n---")
    ali_pub = eg_gen_alice.get_public_info()
    verifications = [verify_sig(ali_pub, ali_signatures[0], hashs[0], 'signature 1', 'hash 1'),
                     verify_sig(ali_pub, ali_signatures[0], hashs[1], 'signature 1', 'hash 2')]

    hashSignA = exer_9(eg_gen_alice)
    exer_10(hashSignA, eg_gen_beto)
    exer_11_12()

if __name__ == '__main__':
    main()

