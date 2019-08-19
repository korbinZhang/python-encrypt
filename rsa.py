# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 frey <summeriwiner@gmail.com>
# blog:https://www.vhcffh.com
#
# Distributed under terms of the MIT license.
import random


# 判断是否是素数
def is_prime(n):
    if n == 2:
        return True
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
    return True


# 生成两个不同的素数p,q
def get_pq():
    p, q = 0, 0
    while True:
        p, q = random.randint(10, 100), random.randint(10, 100)
        if is_prime(p) and is_prime(q) and p != q:
            return p, q


# 生成e和d
def get_ed(p, q):
    phn = (p - 1) * (q - 1) # n的欧拉函数
    while True:
        e = random.randint(2, 50)
        if is_prime(e):
            for d in range(2, 1000):
                if e * d % phn == 1:
                    return e, d


if __name__ == '__main__':
    p, q = get_pq()
    n = p * q
    e, d = get_ed(p, q)
    print("公钥: (n,e) =", (n, e))
    print("私钥: (n,d) =", (n, d))
    m = [random.randint(2, 100) for i in range(10)]
    c = [mi ** e % n for mi in m]
    print("明文 m =", m)
    print("密文 c =", c)
    print("解密 m =", [ci ** d % n for ci in c])
