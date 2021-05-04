#!/usr/bin/env python3
import pickle, base64

class Node():

    def __init__(self):
        print('fake node to bypass attribute-not-found error in pickle.load')

def decode(node, data):
    flag = ''
    cur = node

    for i in range(len(data)):
        if not cur.left and not cur.right:
            flag += cur.data
            cur = node

        if data[i] == '0':
            cur = cur.left
        else:
            cur = cur.right

    if not cur.left and not cur.right:
        flag += cur.data

    return flag

if __name__ == '__main__':

    encoded_data = '110110101000111001001100011010000100101011110101100110100011001110100100011001110000100011101000001001010111011010111110001101101001000001011010110011011001110010111010011010110011001010111011011011010000001110100100001011111101010011001000011000001111110100001011111000100001101011101011110010000101111001111101001010010001001110100100000101110101001111101100011101110001111101111010101111101000010011000111110010110111111000010011111111001111111011011010000100111100111010111011100011011111100010100011110101010011111110011110100110101100010101111011111110110100010101000110110111001000011011111101110101001111110111001001100011101111011100100101010010001100001110101000011000010001110100001001011110101011101011111110000010011000000'

    node = pickle.load(open('node_data.txt', 'rb'))

    flag = decode(node, encoded_data)
    print('huffman decoded:', flag)
    print('flag:', base64.b64decode(flag).decode())
