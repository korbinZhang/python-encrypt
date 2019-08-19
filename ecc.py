# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 frey <summeriwiner@gmail.com>
# blog:https://www.vhcffh.com
#
# Distributed under terms of the MIT license.

"""
椭圆加密算法中的椭圆和基点是公开的
例如国密SM2的公开参数
推荐使用素数域256位椭圆曲线。
椭圆曲线方程：y ^ 2 = x ^ 3 + ax + b。
曲线参数：
p  = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFF
a  = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFC
b  = 28E9FA9E 9D9F5E34 4D5A9E4B CF6509A7 F39789F5 15AB8F92 DDBCBD41 4D940E93
n  = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF 7203DF6B 21C6052B 53BBF409 39D54123
Gx = 32C4AE2C 1F198119 5F990446 6A39C994 8FE30BBF F2660BE1 715A4589 334C74C7
Gy = BC3736A2 F4F6779C 59BDCEE3 6B692153 D0A9877C C62A4740 02DF32E5 2139F0A0
"""
import random


def inv_mod(b, p):
    if b < 0 or p <= b:
        b = b % p
    c, d = b, p
    uc, vc, ud, vd, temp = 1, 0, 0, 1, 0
    while c != 0:
        temp = c
        q, c, d = d // c, d % c, temp
        uc, vc, ud, vd = ud - q * uc, vd - q * vc, uc, vc

    assert d == 1
    if ud > 0:
        return ud
    else:
        return ud + p


def leftmost_bit(x):
    assert x > 0
    result = 1
    while result <= x:
        result = 2 * result
    return result // 2


class CurveFp(object):

    def __init__(self, p, a, b):
        """ 椭圆曲线方程y^2 = x^3 + a*x + b (mod p)."""
        self.p = p
        self.a = a
        self.b = b

    def contains_point(self, x, y):
        return (y * y - (x * x * x + self.a * x + self.b)) % self.p == 0

    def show_all_points(self):
        return [(x, y) for x in range(self.p) for y in range(self.p) if
                (y * y - (x * x * x + self.a * x + self.b)) % self.p == 0]

    def __repr__(self):
        return "Curve(p={0:d}, a={1:d}, b={2:d})".format(self.p, self.a, self.b)

    # def plain_embed(self, x):
    #     if x > self.p:
    #         assert False
    #     for i in range(self.p):
    #         y = (x ** 3 + self.a * x + self.b) ** (1/2)
    #         if int(y) - y == 0:
    #             return Point(self, x, int(y))


class Point(object):

    def __init__(self, curve, x, y, order=None):

        self.curve = curve
        self.x = x
        self.y = y
        self.order = order
        # self.curve is allowed to be None only for INFINITY:
        if self.curve:
            assert self.curve.contains_point(x, y)
        if order:
            assert self * order == INFINITY

    def __eq__(self, other):
        """两个点是否重合"""
        if self.curve == other.curve \
                and self.x == other.x \
                and self.y == other.y:
            return True
        else:
            return False

    def __add__(self, other):
        """两个点‘相加’"""

        if other == INFINITY:
            return self
        if self == INFINITY:
            return other
        assert self.curve == other.curve

        if self.x == other.x:
            if (self.y + other.y) % self.curve.p == 0:
                return INFINITY
            else:
                return self.double()

        p = self.curve.p
        l = ((other.y - self.y) * \
             inv_mod(other.x - self.x, p)) % p

        x3 = (l * l - self.x - other.x) % p
        y3 = (l * (self.x - x3) - self.y) % p

        return Point(self.curve, x3, y3)

    def __mul__(self, other):
        e = other
        if self.order:
            e = e % self.order
        if e == 0:
            return INFINITY
        if self == INFINITY:
            return INFINITY

        e3 = 3 * e
        negative_self = Point(self.curve, self.x, -self.y, self.order)
        i = leftmost_bit(e3) // 2
        result = self

        while i > 1:
            result = result.double()
            if (e3 & i) != 0 and (e & i) == 0:
                result = result + self
            if (e3 & i) == 0 and (e & i) != 0:
                result = result + negative_self
            i = i // 2
        return result

    def __rmul__(self, other):
        """一个点乘以一个整数"""
        return self * other

    def __repr__(self):
        if self == INFINITY:
            return "infinity"
        return "({0},{1})".format(self.x, self.y)

    def double(self):
        """the double point."""
        if self == INFINITY:
            return INFINITY

        p = self.curve.p
        a = self.curve.a
        l = ((3 * self.x * self.x + a) * \
             inv_mod(2 * self.y, p)) % p

        x3 = (l * l - 2 * self.x) % p
        y3 = (l * (self.x - x3) - self.y) % p

        return Point(self.curve, x3, y3)

    def invert(self):
        if self.y is None:
            return Point(None, None, None)
        return Point(self.curve, self.x, -self.y % self.curve.p)




INFINITY = Point(None, None, None)

if __name__ == '__main__':
    p, a, b = 29, 4, 20
    curve = CurveFp(p, a, b)
    G = Point(curve, 3, 1)  # 38
    k = 33  # 私钥
    K = k * G  # 公钥
    print("(公开)椭圆曲线E{}({},{})".format(p, a, b))
    print("(公开)基点G{}".format(G))
    print("私钥: k =", k)
    print("公钥: K =", K)
    m = [Point(curve, 6, 17), Point(curve, 10, 4), Point(curve, 10, 25), Point(curve, 24, 7), Point(curve, 5, 7)]
    print("明文: m=", m)
    # mp = [curve.plain_embed(i) for i in m]
    # print("明文嵌入: mp=", mp)
    # 公钥K加密
    r = [random.randint(2,38) for i in m]
    C1 = [i + ri * K for ri,i in zip(r,m)]
    C2 = [ri * G for ri,i in zip(r,m)]
    print("密文 C1 =", C1)
    print("密文 C2 =", C2)
    print("解密 mm =", [c1 + k*c2.invert() for c1, c2 in zip(C1, C2)])

