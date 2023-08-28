# -*- coding: utf-8 -*-
from myhdl import *


@block
def exe1(q, a, b):
    """
    q = a or !b
    """

    @always_comb
    def comb():
        q.next = a or not b

    return instances()
