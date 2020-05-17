#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
    Esqueleto para o EP1 de Cripto 2020
    Prof. Routo Terada
    Monitor: Thales Paiva

    Exemplo de como rodar o arquivo e saída do programa:
    [~/cripto-2020/ep1]$ sage ep1_esqueleto.py documento.txt
    O Hash SHA512 do arquivo documento.txt é
    dd8996d0f9f8c17056ab3314105ca4043ef729adf8b0f5f84e0d71ef8e51765cfa58741df01aaa5ae5642c54ecf47b2de02140f95956d3d6370e2ade18ef7a13
    O inteiro correspondente ao hash para uso no ElGamal é
    11602858124117136456103271775114122754696733789413816382276456553852239770973923409586227117425499556575579222816159862027314152111415107121278401054210579
    A distância de Hamming entre 0x4123 e 0x3189 é
    7
"""

from sage.all import *

import sys
import hashlib


# Parâmetros públicos p e g
PRIME = 3329499024484696430955445194464218832905973351121497617435753366182222251575714808510036328892050841
GENERATOR = 17


def elgamal_keygen():

    # Calcula os valores abaixo como explicado
    secret_key = None
    public_key = None

    return secret_key, public_key


def elgamal_sign(message, secret_key):

    # Calcula os valores abaixo como explicado
    r = None
    s = None

    return (r, s)


def elgamal_verify(signature, message, public_key):

    # Deve devolver True se assinatura for válida e False se não for
    return None


def get_binary_representation_512_bits_of_hex(h):
    '''
    Recebe uma string h representando um hexadecimal.
    Devolve a representação binária de h com EXATAMENTE 512 bits
    '''

    bin_h = bin(int(h, 16))[2:]  # [2:] Tira o 0b da frente
    bin_h_512bits = '0' * (512 - len(bin_h)) + bin_h

    return bin_h_512bits


def hamming_distance_with_hex_strings(h1, h2):
    """
    Calcula a distância de hamming entre dois hashes em STRINGS representando
    hexadecimais
    """

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


def main():
    """
    Função principal que ordena as chamadas de funções para realizar o que foi
    pedido no EP.
    """
    if len(sys.argv) != 2:
        print('Uso: %s <documento>' % sys.argv[0])
        sys.exit(1)

    # Abaixo mostro como calcular o hash de um arquivo:
    filepath = sys.argv[1]
    sha512_file(filepath)

    filehash = sha512_file(filepath)
    print('O Hash SHA512 do arquivo %s é' % (filepath))
    print(filehash)

    print('O inteiro correspondente ao hash para uso no ElGamal é')
    print(int(filehash, 16))

    print('A distância de Hamming entre 0x4123 e 0x3189 é')
    print(hamming_distance_with_hex_strings('0x4123', '0x3189'))

if __name__ == '__main__':
    main()

