# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 frey <summeriwiner@gmail.com>
# blog:https://www.vhcffh.com
#
# Distributed under terms of the MIT license.
def Md5sum(message: bytes) -> bytes:
    # 定义常量，用于初始化128位变量，注意字节顺序，A=0x01234567，这里低值存放低字节，
    # 即01 23 45 67，所以运算时A=0x67452301，其他类似。
    # 用字符串的形势，是为了和hex函数的输出统一，hex(10)输出为'0xA',注意结果为字符串。
    h0 = 0x67452301
    h1 = 0xefcdab89
    h2 = 0x98badcfe
    h3 = 0x10325476

    # 定义每轮中循环左移的位数，用元组表示 4*4*4=64
    R = (7, 12, 17, 22) * 4 + (5, 9, 14, 20) * 4 + \
        (4, 11, 16, 23) * 4 + (6, 10, 15, 21) * 4
    # 定义常数K 64
    # K[i] = (int(abs(math.sin(i + 1)) * 2 ** 32)) & 0xffffffff
    K = (0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
         0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8,
         0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193,
         0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51,
         0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
         0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905,
         0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681,
         0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60,
         0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
         0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244,
         0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92,
         0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314,
         0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391)

    # 定义每轮中用到的函数。L为循环左移，
    # 左移之后可能会超过32位，所以要和0xffffffff做与运算，确保结果为32位。
    F = lambda x, y, z: ((x & y) | ((~x) & z))
    G = lambda x, y, z: ((x & z) | (y & (~z)))
    H = lambda x, y, z: (x ^ y ^ z)
    I = lambda x, y, z: (y ^ (x | (~z)))

    L = lambda x, n: ((x << n) | (x >> (32 - n))) & 0xffffffff
    # 小端  0x12,0x34,0x56,0x78 -> 0x78563412
    # 将四个8位无符号数转化为一个32位无符号数
    W = lambda i4, i3, i2, i1: (i1 << 24) | (i2 << 16) | (i3 << 8) | i4
    # 字节翻转 0x12345678 -> 0x78563412 将一个32位无符号数的高位和低位进行对换
    reverse = lambda x: (x << 24) & 0xff000000 | (x << 8) & 0x00ff0000 | \
                        (x >> 8) & 0x0000ff00 | (x >> 24) & 0x000000ff


    # 对每一个输入先添加一个'0x80'，即'10000000', 即128
    ascii_list = list(map(lambda x: x, message))
    msg_length = len(ascii_list) * 8
    ascii_list.append(128)

    # 补充0
    while (len(ascii_list) * 8 + 64) % 512 != 0:
        ascii_list.append(0)

    # 最后64为存放消息长度，以小端数存放。
    # 例如，消息为'a'，则长度是8，则添加'0x0800000000000000'
    for i in range(8):
        ascii_list.append((msg_length >> (8 * i)) & 0xff)

    # print(ascii_list)
    # print(len(ascii_list)//64)
    # 对每一消息块进行迭代
    for i in range(len(ascii_list) // 64):
        # print(ascii_list[i*64:(i+1)*64])
        # 对每一个消息块进行循环，每个消息块512bits=16*32bits=64*8bits
        a, b, c, d = h0, h1, h2, h3
        for j in range(64):
            # 64轮的主循环
            if 0 <= j <= 15:
                f = F(b, c, d) & 0xffffffff
                g = j
            elif 16 <= j <= 31:
                f = G(b, c, d) & 0xffffffff
                g = ((5 * j) + 1) % 16
            elif 32 <= j <= 47:
                f = H(b, c, d) & 0xffffffff
                g = ((3 * j) + 5) % 16
            else:
                f = I(b, c, d) & 0xffffffff
                g = (7 * j) % 16
            aa, dd, cc = d, c, b
            # 第i个chunk，第g个32-bit
            s = i * 64 + g * 4
            w = W(ascii_list[s], ascii_list[s + 1], ascii_list[s + 2], ascii_list[s + 3])
            bb = (L((a + f + K[j] + w) & 0xffffffff, R[j]) + b) & 0xffffffff
            a, b, c, d = aa, bb, cc, dd
            # print(b)
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
    h0, h1, h2, h3 = reverse(h0), reverse(h1), reverse(h2), reverse(h3)
    digest = (h0 << 96) | (h1 << 64) | (h2 << 32) | h3
    return hex(digest)[2:].rjust(32, '0')


if __name__ == '__main__':
    print("自己实现md5(b'https://www.vhcffh.com')")
    print(Md5sum(b"https://www.vhcffh.com"))

    import hashlib
    t = hashlib.md5()
    t.update(b"https://www.vhcffh.com")
    print("调用hashlib库md5(b'https://www.vhcffh.com')")
    print(t.hexdigest())
