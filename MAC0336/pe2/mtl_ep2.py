from sage.all import *

import sys
import binascii
import codecs
import sys
import hashlib

from os import urandom
import os
import codecs

PRIME = 263

chosen_k = set([0])
field = None
infinity_point = None

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

def gen_docs(docss):
    docs = docss
    nusps = ['9793714', '9793715']
    r_str = urandom(10**3) #100kB of random bytes
    sha512_hashs = [-1,-1]
    for ind in [0,1]:
        print('File: %s' % docs[ind])
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

def encrypit_files(docs, public_key):
    encs = []
    for filename in docs:
        k = sample_k(public_key)
        f = open(filename, 'rb')
        read_b = f.read()
        f.close()
        encs.append(CBC_MV_encrypt(read_b, public_key, k))
        print("First 50 encripted blocks (~100bytes) of %s:" % filename)
        for i in range (50):
            f = hex(encs[-1][i][1].lift())
            if len(f) == 0:
                f = "00"
            elif len(f) == 1:
                f = "0" + f
            s = hex(encs[-1][i][2].lift())
            if len(s) == 0:
                s = "00"
            elif len(s) == 1:
                s = "0" + s
            print (f + s),
        print
    return encs

def sample_k(public_key):
    global field, chosen_k
    while (True):
        while (True):
            k = field.random_element()
            if k not in chosen_k:
                chosen_k.add(k)
                break
        if (k.lift() * public_key[1] != infinity_point):
            break;
    return k
def MV_encrypt(X, public_key, k=None):
    global field, chosen_k
    if k is None:
        k = sample_k(public_key)
    y0 = k.lift() * public_key[0]
    (c1,c2) = (k.lift() * public_key[1]).xy()
    y1 = (c1 * X[0]) % PRIME
    y2 = (c2 * X[1]) % PRIME
    return (y0, y1, y2)

def CBC_MV_encrypt(big_message, public_key, k=None):
    # X da forma (0-262, 0-262)
    # Lerei blocos com 8 bits para ter valores 0-256
    hex_message = binascii.hexlify(big_message)
    if len(hex_message)%2 != 0:
        hex_message += '0'
    # each index has the string representation of a byte in hexadecimal
    blocks = [int(hex_message[i:i+2], 16) for i in range(0, len(hex_message), 2)]
    VI = 0
    z = [(blocks[0], blocks[1])]
    res = MV_encrypt(z[0], public_key, k)
    y = [res]
    for i in range (2, len(blocks) - 1, 2):
        y1 = y[-1][1].lift()
        y2 = y[-1][2].lift()
        z.append((y1.__xor__(blocks[i]), y2.__xor__(blocks[i+1])))
        res = MV_encrypt(z[-1], public_key, k)
        y.append(res)
    return y


def MV_decrypt(Y, public_key, private_key):
    (c1, c2) = (private_key * Y[0]).xy()
    x1 = (Y[1] * inverse_mod(c1.lift(), PRIME)) % PRIME
    x2 = (Y[2] * inverse_mod(c2.lift(), PRIME)) % PRIME
    return (x1, x2)

def CBC_MV_decrypt(big_ciphertext, public_key, private_key):
    # X of (0-262, 0-262)
    # big_ciphertext is such array of Xs
    z = [MV_decrypt(big_ciphertext[0], public_key, private_key)]
    x = [(z[0][0].lift(), z[0][1].lift())]
    for i in range (1, len(big_ciphertext)):
        z.append(MV_decrypt(big_ciphertext[i], public_key, private_key))
        z1 = z[-1][0].lift(); z2 = z[-1][1].lift()
        y1 = big_ciphertext[i-1][1].lift()
        y2 = big_ciphertext[i-1][2].lift()
        x.append((z1.__xor__(y1),
                  z2.__xor__(y2)))
    # return big_message
    return x


def get_binary_representation_512_bits_of_hex(bin_h):
    bin_h_512bits = '0' * (512 - len(bin_h)) + bin_h

    return bin_h_512bits


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

# Does not deal with either p1 or p2 being points at infinity
def point_addition (p1, p2, a, md):
    if p1[0] == p2[0] and p2[1] == -p1[1]: return infinity_point
    if p1 == p2:
        t = (3*(p1[0]**2) + a) * Integer(2*p1[1]).inverse_mod(md)
    else:
        t = (p2[1] - p1[1]) * Integer(p2[0] - p1[0]).inverse_mod(md)
    t%=md
    xr = (t**2 - p1[0] - p2[0]) % md
    yr = (t*(p1[0] - xr) - p1[1]) % md
    return (xr, yr)

def main():
    if len(sys.argv) != 2:
        print("Usage: One arguments - documentoX (unused)")
        sys.exit(0)
    global field, chosen_k, infinity_point
    x,y=var('x y')
    field = Integers(263)
    E = EllipticCurve(field, [2,3])
    infinity_point = E(0)
    P = (200, 39)
    P_el = E(P)
    R = (175, 80)
    # Equialent to using E(P), except it does not throw exceptions
    #  if number does not belong
    belongs = fast_callable(x**3 + 2*x +3 - y**2, vars=[x,y], domain=field)
    pts = E.points() #sorted list of points
    print("2. P = (200,39) belongs to curve? " + str(belongs(P[0], P[1]) == 0))
    print("3. The curve has %d points" % E.count_points())
    print("4. The first 10 points:")
    for i in range (10): print(pts[i]) 
    print("5. R = %s belongs to curve? %s" % (str(R), str(belongs(R[0], R[1]) == 0)))
    sumpr = point_addition(P,R,2,263)
    print("6. P + R = %s" % str(sumpr))
    s = 9793714%263
    print("7. s = %d mod%d = %d" % (9793714, 263, s))
    Q = s * P_el
    print("8. sP = %d*%s = Q = %s" % (s, P_el, Q))
    cripted = MV_encrypt(R, (P_el, Q))
    print("9. The encryption of R is %s" % str(cripted))
    decripted = MV_decrypt(cripted, (P_el, Q), s)
    print("10. The de-cryption is %s" % str(decripted))
    print("11 / 15. File gen and hashs")
    gen_docs(["documento1", "documento2"])
    print("12 / 16. Crypt documents:")
    encs = encrypit_files(["documento1", "documento2"], (P_el, Q))
    encs_str = ["", ""]
    print("First 50 blocks decrypted")
    for j in range (2):
        for i in range (len(encs[j])):
            f = hex(encs[j][i][1].lift())
            if len(f) == 0:
                f = "00"
            elif len(f) == 1:
                f = "0" + f
            sec = hex(encs[j][i][2].lift())
            if len(sec) == 0:
                sec = "00"
            elif len(sec) == 1:
                sec = "0" + sec
            encs_str[j] += f + sec
    print("13. Decrypt cripted doc1:")
    decri = CBC_MV_decrypt(encs[0], (P_el, Q), s)
    decri_str = ""
    print("First 50 blocks decrypted")
    for i in range (len(decri)):
        f = hex(decri[i][0])
        if len(f) == 0:
            f = "00"
        elif len(f) == 1:
            f = "0" + f
        s = hex(decri[i][1])
        if len(s) == 0:
            s = "00"
        elif len(s) == 1:
            s = "0" + s
        decri_str += f + s
    print(decri_str[0:200])
    print("14. Distance is %d. The result shows big difference and this is desired, "
        "because the encryption should be very different from the original"\
        % hamming_distance_with_hex_strings(encs_str[0], decri_str))
    print("17. Distance is %d. The result shows big difference and this is desired, "
        "because the encryption of similar texts should be very different"\
        % hamming_distance_with_hex_strings(encs_str[0], encs_str[1]))
    s2 = 93
    QB = s2 * P_el
    print("18. Beto's Q is: s2 * P = 93 * P = %s" % str(QB))
    print("19. Crypt document1:")
    b_encr = encrypit_files(["documento1"], (P_el, QB))[0]
    b_encr_s = ""
    for i in range (len(b_encr)):
        f = hex(b_encr[i][1].lift())
        if len(f) == 0:
            f = "00"
        elif len(f) == 1:
            f = "0" + f
        sec = hex(b_encr[i][2].lift())
        if len(sec) == 0:
            sec = "00"
        elif len(sec) == 1:
            sec = "0" + sec
        b_encr_s += f + sec
    print("20. Hamming distance is %d. I think the distance in itself does not "\
        "show anything." % hamming_distance_with_hex_strings(b_encr_s, encs_str[0]))
    
if __name__ == '__main__':
    main()
