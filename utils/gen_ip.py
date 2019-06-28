# -*- coding:utf-8 -*-
"""
gen ips by ip and count
"""


class GenIps:
    @staticmethod
    def i2n(i):
        """
        ip to num
        :param i: ip
        :return:
        """
        ip = [int(x) for x in i.split('.')]
        return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

    @staticmethod
    def n2i(n):
        """
        num to ip
        :param n: num
        :return:
        """
        return '%s.%s.%s.%s' % (
            (n & 0xff000000) >> 24,
            (n & 0x00ff0000) >> 16,
            (n & 0x0000ff00) >> 8,
            (n & 0x000000ff)
        )

    def gen(self, s, c):
        """

        :param s: start ip such as 192.168.10.20
        :param c: count for ips
        :return: ip list
        """

        return [self.n2i(self.i2n(s) + n) for n in range(int(c))]


if __name__ == '__main__':
    test = GenIps()
    res = test.gen("192.168.0.250", 10)
    print(res)
