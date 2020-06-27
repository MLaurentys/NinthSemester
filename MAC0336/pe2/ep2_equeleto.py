"""
    Esqueleto para o EP2 de Cripto 2020
    Prof. Routo Terada
    Monitor: Thales Paiva

    Para rodar:
    [~/cripto-2020/ep1]$ sage ep1_esqueleto.py
"""

from sage.all import *

import sys


# Parâmetro público p: a característica do corpo finito usado para instanciar
# a curva elíptica
PRIME = 263


def MV_keygen():

    # Calcula os valores:
    #   public_key = (Q, P) \in E^2
    #   secret_key = s tal que Q = sP
    secret_key = None
    public_key = None

    return secret_key, public_key


# Função de encriptação simples (DE UM BLOCO)
def MV_encrypt(X, public_key):

    # Calcula o valor de Y = (y0, y1, y2) como descrito no enunciado

    # return Y
    return None


# Função de encriptação usando modo CBC
# (quebra uma mensagem grande em blocos e encripta sequencialmente sob o regime
# CBC - cipher block chaining)
def CBC_MV_encrypt(big_message, public_key):

    # Boa sorte

    # return (Y1, Y2, Y3, ...)
    return None


def MV_decrypt(Y, public_key):
    # Calcula o valor de X = (x1, x2) como descrito no enunciado

    # return X
    return None


# Função de decriptação usando modo CBC
# (quebra uma mensagem grande em blocos e decripta sequencialmente na ordem
# certa sob o regime CBC - cipher block chaining)
def CBC_MV_decrypt(big_ciphertext, public_key):

    # Boa sorte_2

    # return big_message
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


def main():
    E = EllipticCurve(Intergers(263), [2,3])
    belongs = fast_callable(x^3 + 2*x +3 - y^2, vars=[x,y])
    print("(200,39) belongs to curve?", belongs(200, 39) == 0)


if __name__ == '__main__':
    main()
