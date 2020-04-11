#! /usr/bin/python3.7
# -*- coding: utf-8 -*-
# Module request: Util(self)
# Author: w366er
from w366er_tool import Util

"""
Description:
1. Implement of normal AES-128
2. Steps:
    1. Key Addition
    2. Bytes Substitution(S-box)
    3. Shift Rows
    4. Mix Columns
"""


class AES:
    def __init__(self):
        self.round_key_box = []
        self.plaintext_box = []
        self.row_confusion_box = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
        self.inv_row_confusion_box = [0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3]
        self.column_confusion_box = [[0x02, 0x03, 0x01, 0x01],
                                     [0x01, 0x02, 0x03, 0x01],
                                     [0x01, 0x01, 0x02, 0x03],
                                     [0x03, 0x01, 0x01, 0x02]
                                     ]
        self.inv_column_confusion_box = [[0x0e, 0x0b, 0x0d, 0x09],
                                         [0x09, 0x0e, 0x0b, 0x0d],
                                         [0x0d, 0x09, 0x0e, 0x0b],
                                         [0x0b, 0x0d, 0x09, 0x0e]
                                         ]
        self.s_box = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
                      [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
                      [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
                      [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
                      [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
                      [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
                      [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
                      [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
                      [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
                      [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
                      [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
                      [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
                      [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
                      [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
                      [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
                      [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
                      ]

        self.inv_s_box = [[0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7,
                          0xfb],
                          [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9,
                          0xcb],
                          [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3,
                          0x4e],
                          [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1,
                          0x25],
                          [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6,
                          0x92],
                          [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d,
                          0x84],
                          [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45,
                          0x06],
                          [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a,
                          0x6b],
                          [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
                          0x73],
                          [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf,
                          0x6e],
                          [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe,
                          0x1b],
                          [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a,
                          0xf4],
                          [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec,
                          0x5f],
                          [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c,
                          0xef],
                          [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99,
                          0x61],
                          [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
                          ]
        self.rcon_box = [0x00, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

    def g_function(self, g_f_key, r):

        # Divide the g_f_key with the Order 1, 2, 3, 0
        temp_box = []
        for i in range(1, 4):
            temp = g_f_key[8 * i:8 * i + 8]  # 8 bits
            temp_box.append(temp)
        temp_box.append(g_f_key[:8])  # Compensate the First Block

        # S-box Permutation
        temp_box_one = []
        for i in temp_box:
            temp = i
            row = int(temp[0:4], 2)
            line = int(temp[4:8], 2)
            temp = self.s_box[row][line]
            temp = Util.fore_8bits_padding(bin(temp)[2:])
            temp_box_one.append(temp)

        # Xor with Rcon-box
        temp = ""
        temp_one = bin(self.rcon_box[r])[2:]
        temp_one = Util.fore_8bits_padding(temp_one)
        for i in range(len(temp_one)):
            temp += str(int(temp_one[i]) ^ int(temp_box_one[0][i]))
        temp_box_one[0] = temp

        # Return the Four 8-bit Blocks
        temp = ""
        for i in temp_box_one:
            temp += i
        # Test len...
        return temp

    def generate_key(self, g_key):

        # Change to 128-bit Binary
        bin_key = bin(int(g_key, 16))[2:]
        bin_key = Util.fore_8bits_padding(bin_key)

        # Get w1, w2, w3, w4(Round Key Box)
        for i in range(4):
            temp = bin_key[32 * i: 32 * i + 32]
            self.round_key_box.append(temp)

        # Generate Other Round Keys
        for i in range(4, 44):
            temp = self.round_key_box[i - 1]  # 32-bits
            if i % 4 == 0:
                temp = self.g_function(temp, i // 4 - 1)
            temp_one = ""
            for j in range(len(temp)):
                temp_one += str(int(temp[j]) ^ int(self.round_key_box[i - 4][j]))
            self.round_key_box.append(temp_one)

    def row_shift_permutation(self):
        # Shift
        temp_row_shift_box = []
        for i in self.row_confusion_box:
            temp_row_shift_box.append(self.plaintext_box[i])
        self.plaintext_box = temp_row_shift_box

    @staticmethod
    def gmult(a, b):  # Confused
        p = 0
        for c in range(8):
            if b & 1:
                p ^= a
            a <<= 1
            if a & 0x100:
                a ^= 0x11b
            b >>= 1
        return p

    def column_confusion_permutation(self):
        a = self.column_confusion_box
        b = self.plaintext_box
        for i in range(4):
            for j in range(4):
                temp_one = self.gmult(a[j][0], int(b[4 * i + 0], 2))  # a is int, b is a 8-bit string
                temp_two = self.gmult(a[j][1], int(b[4 * i + 1], 2))
                temp_three = self.gmult(a[j][2], int(b[4 * i + 2], 2))
                temp_four = self.gmult(a[j][3], int(b[4 * i + 3], 2))
                temp = temp_one ^ temp_two ^ temp_three ^ temp_four
                temp = bin(temp)[2:]
                temp = Util.fore_8bits_padding(temp)
                self.plaintext_box[i * 4 + j] = temp
                # Seems to be solved

    def encrypt(self):

        # Input the Key and Plaintext
        key = "2b7e151628aed2a6abf7158809cf4f3c"
        plain_text = "3243f6a8885a308d313198a2e0370734"  # Stop here

        # Change to 128-bit Binary
        bin_plaintext = bin(int(plain_text, 16))[2:]  # 128 bits
        bin_plaintext = Util.fore_8bits_padding(bin_plaintext)

        # Split Plaintext
        # Generate Round Keys
        self.generate_key(key)

        # The First Round Key Addition
        round_key = ""
        temp = ""
        for i in range(4):
            round_key += self.round_key_box[i]  # 128 bits
        for i in range(len(round_key)):
            temp += str(int(round_key[i]) ^ int(bin_plaintext[i]))
        bin_plaintext = temp

        # Ten Rounds Encryption
        for i in range(10):

            # Divide the plaintext into 16 Blocks
            for j in range(16):
                self.plaintext_box.append(bin_plaintext[j * 8:j * 8 + 8])

            # Byte Replacement with S-box
            for j in range(16):
                temp = self.plaintext_box[j]
                row = int(temp[0:4], 2)
                line = int(temp[4:8], 2)
                temp = bin(self.s_box[row][line])[2:]
                temp = Util.fore_8bits_padding(temp)
                self.plaintext_box[j] = temp

            # Row Shift Permutation
            self.row_shift_permutation()

            # Column Confusion Permutation
            if i != 9:
                self.column_confusion_permutation()
                # Test
                # print(i)
                # for j in self.plaintext_box:
                #     print(j)

            # Xor With the Round Key
            round_key = ""
            temp = ""
            for j in range((i + 1) * 4, (i + 2) * 4):
                round_key += self.round_key_box[i]
            for j in range(16):
                bin_plaintext += self.plaintext_box[j]  # 8 bits per in plaintext box
            for j in range(len(round_key)):
                temp += str(int(round_key[j]) ^ int(bin_plaintext[j]))
            bin_plaintext = temp

        print(hex(int(bin_plaintext, 2)))


me = AES()
me.encrypt()