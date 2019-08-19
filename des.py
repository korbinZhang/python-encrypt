# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 frey <summeriwiner@gmail.com>
# blog:https://www.vhcffh.com
#
# Distributed under terms of the MIT license.
IP = (58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7)
FP = (40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25)
E = (32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1)
P = (16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25)
S = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
      [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
      [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
      [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

     [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
      [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
      [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
      [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

     [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
      [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
      [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
      [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

     [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
      [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
      [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
      [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

     [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
      [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
      [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
      [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

     [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
      [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
      [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
      [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

     [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
      [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
      [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
      [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

     [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
      [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
      [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
      [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
PC_1L = (57, 49, 41, 33, 25, 17, 9,
         1, 58, 50, 42, 34, 26, 18,
         10, 2, 59, 51, 43, 35, 27,
         19, 11, 3, 60, 52, 44, 36)
PC_1R = (63, 55, 47, 39, 31, 23, 15,
         7, 62, 54, 46, 38, 30, 22,
         14, 6, 61, 53, 45, 37, 29,
         21, 13, 5, 28, 20, 12, 4)
PC_2 = (14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32)


def Permute(block, b_len, PP):
    # 通过置换矩阵PP对block进行置换,b_len是块长度(位，bit)
    res = 0
    for i in PP:
        res = res << 1
        # 第i-1的位置 即倒数第
        res |= (block >> (b_len - i)) & 0x01
    return res


def bytesToblocks(m):
    # 字节序列转换位blocks    b'\x00\x01\x02\x03\xff\xff\xff\xff' -> [0x00010203,0xffffffff]
    while len(m) % 8 != 0:
        m += b'\x00'
    blocks = []
    for i in range(len(m) // 4):
        blocks.append((m[4 * i] << 24) | (m[4 * i + 1] << 16) |
                      (m[4 * i + 2] << 8) | (m[4 * i + 3]))
    return blocks


def blocksTobytes(blocks):
    # blocks转换为字节序列    [0x00010203,0xffffffff] -> b'\x00\x01\x02\x03\xff\xff\xff\xff'
    res = b''
    for i in blocks:
        res += i.to_bytes(4, byteorder="big")
    return res


L = lambda x, n: ((x << n) | (x >> (28 - n))) & 0x0fffffff
# 对一个28bits的数x进行循环左移n位

class DES(object):

    def F(self, block, subKeyid):
        """

        :param block: 32bits
        :param subKeyid:
        :return: res: 32bits
        """
        temp = Permute(block, 32, E) ^ self.subKs[subKeyid]
        res = 0
        for i in range(8):
            res = res << 4
            yxxxxy = (temp >> 6 * (7 - i)) & 0x3f
            xxxx = (yxxxxy & 0x1f) >> 1
            yy = ((yxxxxy >> 5) << 1) | (yxxxxy & 0x01)
            res |= S[i][yy][xxxx]
        res = Permute(res, 32, P)
        return res & 0xffffffff

    def __init__(self, K: bytes):
        # 通过密钥K生成实例
        self.K = K
        self.K_blocks = bytesToblocks(K)[:2]
        # 生成字密钥self.subKs[16]
        self.subKs = None
        self.generate_subKs()

    def Encrypt(self, m: bytes) -> bytes:
        # 加密
        blocks = bytesToblocks(m)
        cblocks = []
        for i in range(len(blocks) // 2):
            # 每个64bits的高32bits，低32bits
            high, low = blocks[2 * i], blocks[2 * i + 1]
            # 第一步：初始置换IP
            temp = Permute((high << 32) | low, 64, IP) & 0xffffffffffffffff
            # 第二步：获取 Li 和 Ri
            high, low = temp >> 32, temp & 0xffffffff
            # 第三步：共16轮迭代
            for j in range(16):
                high, low = low, (high ^ self.F(low, j))
            # 第四步：合并L16和R16，注意合并为 R16L16
            high, low = low, high
            # 第五步：末尾置换FP
            temp = Permute((high << 32) | low, 64, FP) & 0xffffffffffffffff
            high, low = temp >> 32, temp & 0xffffffff
            cblocks.append(high)
            cblocks.append(low)
        return blocksTobytes(cblocks)

    def Decrypt(self, e: bytes) -> bytes:
        # 解密
        blocks = bytesToblocks(e)
        cblocks = []
        for i in range(len(blocks) // 2):
            # 每个64bits的高32bits，低32bits
            high, low = blocks[2 * i], blocks[2 * i + 1]
            # 第一步：初始置换IP
            temp = Permute((high << 32) | low, 64, IP) & 0xffffffffffffffff
            # 第二步：获取 Li 和 Ri
            high, low = temp >> 32, temp & 0xffffffff
            # 第三步：共16轮迭代, 子密钥逆序
            for j in range(16):
                high, low = low, (high ^ self.F(low, 15 - j))
            # 第四步：合并L16和R16，注意合并为 R16L16
            high, low = low, high
            # 第五步：末尾置换FP
            temp = Permute((high << 32) | low, 64, FP) & 0xffffffffffffffff
            high, low = temp >> 32, temp & 0xffffffff
            cblocks.append(high)
            cblocks.append(low)
        return blocksTobytes(cblocks)

    def generate_subKs(self):
        # print(bin((self.K_blocks[0] << 32) | self.K_blocks[1])[2:].rjust(32, '0'))
        C = Permute((self.K_blocks[0] << 32) | self.K_blocks[1], 64, PC_1L)  & 0x0fffffff
        D = Permute((self.K_blocks[0] << 32) | self.K_blocks[1], 64, PC_1R)  & 0x0fffffff
        # print(bin(C)[2:].rjust(28, '0'))
        # print(bin(D)[2:].rjust(28, '0'))
        self.subKs = []
        for i in range(16):
            if i in (0, 1, 8, 15):
                C, D = L(C, 1), L(D, 1)
            else:
                C, D = L(C, 2), L(D, 2)
            self.subKs.append(Permute((C << 28) | D, 56, PC_2))
            # print(hex(self.subKs[i]))

    def getK(self) -> bytes:
        # 返回密钥K
        return self.K

    def generateK(self) -> bytes:
        # 随机产生密钥K
        pass


def print_bytes_hex(m):
    for i in m:
        print(hex(i)[2:].rjust(2, '0'), end='')
    print()


if __name__ == '__main__':
    # 密钥不足64bits 添零，多于64bits 使用前64bits
    # messages 不足64bits的倍数 补零
    m = b'https://www.vhcffh.com' # 明文
    k = b'123456' # 密钥 
    a = DES(k)
    cc = a.Encrypt(m)
    mm = a.Decrypt(cc)
    print("明文:", end='')
    print(m)
    print("密钥:", end='')
    print(a.K)
    print("密文:", end='')
    print_bytes_hex(cc)  # 以bytes输出
    print("解密:", end='')
    print(mm)


# http://www.hankcs.com/security/des-algorithm-illustrated.html

