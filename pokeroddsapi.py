import re
from collections import Counter
import itertools
import math
import tabulate
import copy
import time

__all__ = ["CC", "get_cards", "trans", "valhand", "InvalidCardError", "analyze", "binomial_coefficient", "nice_hand"]

SU = "♥♠♣♦"
SUITES = "HSCD"  # Hearts, Spades, Clubs, Diamonds
SUD = dict(zip(SUITES, SU))
SS = "234567890JQKA"
VV = dict(((s, i+2) for i, s in enumerate(SS)))

CC = ["high", "pair", "2pair", "three", "seq", "flush", "full", "four", "", "", "SAMESHIT"]

class InvalidCardError(Exception):
    pass


def binomial_coefficient(n: int, k: int) -> int:
    # https://stackoverflow.com/questions/33959043/get-a-number-of-possible-combinations-python
    n_fac = math.factorial(n)
    k_fac = math.factorial(k)
    n_minus_k_fac = math.factorial(n - k)
    return n_fac/(k_fac*n_minus_k_fac)


def valhand(hand):
    for e in hand:
        if len(e) > 2:
            raise InvalidCardError(f"Size not 2 for '{e}")
        eu = e.upper()
        if eu[0] not in SS:
            raise InvalidCardError(f"Invalid card value: '{e}")
        if len(e) == 2 and eu[1] not in SUITES:
            raise InvalidCardError(f"Invalid card suite: '{e}'")

    hand = [x+("*" if len(x) == 1 else "") for x in hand]
    return hand


def get_cards():
    ret = []
    for suite in SUITES:
        for s in SS:
            ret.append(s+suite)
    return ret


def trans(_hand):
    hand = copy.copy(_hand)
    hand.sort()
    game = 0
    nha = len(hand)

    if nha == 0:
        return game

    numbers, suites = list(["".join(x) for x in zip(*hand)])

    counts = Counter(numbers)
    unique_numbers = unu = list(counts.keys())
    cv = list(counts.values())
    unique_counts = uco = cv
    n = len(unu)

    if 4 in cv:
        game = 7
    elif 3 in cv:
        if 2 in counts:
            game = 6
        else:
            game = 3
    elif 2 in cv:
        coco = Counter(cv)
        if coco[2] >= 2:
            game = 2
        else:
            game = 1

    if game < 4 and nha >= 5 and len(counts) >= 5:
        nunu = ([1] if "A" in unu else [])+[VV[x] for x in unu]
        nunu.sort()
        isseq = False
        nseq = 0
        for a0, a1 in zip(nunu[:-1], nunu[1:]):
            if a1-a0 > 1:
                nseq = 0
            else:
                nseq += 1
                if nseq == 4:
                    isseq = True
                    break

        if isseq:
            game = 4

    if game < 5 and nha >= 5:
        # counts = Counter(suites)
        # unique_numbers = unu = list(counts.keys())
        # unique_counts = uco = list(counts.values())
        # n = len(unu)
        n = len(set(suites))
        if n == 1 and suites[0] != "*":
            game = 5

    return game

def analyze(hand):
    cards = get_cards()
    for card in hand:
        cards.remove(card)
    nres = 7-len(hand)
    if nres < 0:
        report = "I need at most 7 cards"
    cc = list(itertools.combinations(cards, nres))
    ncc = len(cc)
    hh5 = []
    hh7 = []
    ii = 0
    iii = 0
    t = time.time()
    for c in cc:
        handall = hand+list(c)
        h5 = trans(handall[2:])
        h7 = trans(handall)
        hh5.append(h7 if h7 > h5 else 10)
        hh7.append(h7)
        # hhh.append(highest7(hand, list(c)))

        ii += 1
        iii += 1
        if iii == 1000:
            print(f"{ii+1}/{ncc}")
            iii = 0
    print(f"🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖 analyze {time.time()-t:.3} 🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖🕖")


    ch5 = Counter(hh5)
    ch7 = Counter(hh7)
    n = sum(ch5.values())

    uch = set(ch5.keys()).union(ch7.keys())


    hh = ["feature", "possibilities", "of", "total", "", "%", "possibilities", "of", "total", "", "%"]
    dd = []
    for key in uch:
        dd.append([CC[key]]+
                   ([None, None, None, None] if key not in ch5 else [ch5[key], n, ch5[key]/n*100, "%"])+
                   ([None, None, None, None] if key not in ch7 else [ch7[key], n, ch7[key]/n*100, "%"]))
    report = tabulate.tabulate(dd, hh)

    return report


def nice_hand(hand):
    hand_ = [x[0]+SUD[x[1]] for x in hand]
    hand__ = " ".join(hand_)
    return hand__