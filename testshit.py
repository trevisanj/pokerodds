import re
from pokeroddsapi import *
import traceback


# hand = ['AC', '3S', "2C", "7D", "AD", "AS"]
hand = ['AC', '2S', "3C", "4D", "5S"]
# hand = ['AC', '3S', "3C", "7D", "AS"]
ik = 0
while True:
    print("(*) BEGIN (*)")
    print("♠♥♦♣ "+CC[trans(hand)]+" ♤♡♢♧")
    n = len(hand)
    nc0 = int(binomial_coefficient(52 - n, 7 - n))
    nc1 = int(nc0*binomial_coefficient(7, 5))
    print(f"Number of combinations: {nc0}")
    print("(*) END (*)")

    question = f"{nice_hand(hand)} >> "
    if ik == 0:
        s = "@"
        print(f"{question}{s}")
    else:
        s = input(question)
        if re.match("[~!@#$%^&*()_\-+=]\w", s):
            s = s[0]+" "+s[1:]

    ik += 1

    try:
        flag_add = False
        p = False
        if s:
            a = [x.strip().upper() for x in s.split()]
            if a[0] == "@":
                p = True
                print("(A) BEGIN (A)")
                print(analyze(hand))
                print("(A) END (A)")

            if a[0] == "+":
                _hand = a[1:]
                flag_add = True
            elif a[0] == "-":
                for e in a[1:]:
                    hand.remove(e)
                    p = True
            else:
                _hand = a

            if not p:
                _hand = valhand(_hand)
                if flag_add:
                    for card in _hand:
                        if card in hand:
                            raise InvalidCardError(f"Card '{card}' already in hand")
                    hand += _hand
                else:
                    hand = _hand

    except InvalidCardError as e:
        print("*** BEGIN tachtolo ***")
        print(str(e))
        print("*** END tachtolo ***")
    except:
        print("/*\\")
        traceback.print_exc()
        print("\*/")
