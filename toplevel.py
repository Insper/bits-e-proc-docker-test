#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from myhdl import *

@block
def blinkLed(ledr, clk, rst):
    cnt = Signal(intbv(0)[32:])
    l = Signal(bool(0))

    @always_seq(clk.posedge, reset=rst)
    def seq():
        if cnt < 20000000:
            cnt.next = cnt + 1
        else:
            cnt.next = 0
            l.next = not l

        for i in range(len(ledr)):
            ledr[i].next = l

    return instances()


@block
def toplevel(LEDR, CLOCK_50, RESET_N):
    sw_s = [SW(i) for i in range(10)]
    ledr_s = [Signal(bool(0)) for i in range(10)]

    ic2 = blinkLed(ledr_s, CLOCK_50, RESET_N)

    @always_comb
    def comb():
        for i in range(len(ledr_s)):
            LEDR[i].next = ledr_s[i]


    return instances()

LEDR = Signal(intbv(0)[10:])
SW = Signal(intbv(0)[10:])
KEY = Signal(intbv(0)[4:])
HEX0 = Signal(intbv(1)[7:])
HEX1 = Signal(intbv(1)[7:])
HEX2 = Signal(intbv(1)[7:])
HEX3 = Signal(intbv(1)[7:])
HEX4 = Signal(intbv(1)[7:])
HEX5 = Signal(intbv(1)[7:])
CLOCK_50 = Signal(bool())
RESET_N = ResetSignal(1, active=0, isasync=False)

top = toplevel(LEDR, CLOCK_50, RESET_N)
top.convert(hdl="verilog")
