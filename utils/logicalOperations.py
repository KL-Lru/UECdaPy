# Logical Operations -----
# カード行列同士の論理演算

def cardOr(cards1, cards2):
    # cards1とcards2のどちらかに入っているカード
    return ((cards1 + cards2) > 0) * 1

def cardAnd(cards1, cards2):
    # cards1とcards2の両方に含まれているカード
    return ((cards1 * cards2) > 0) * 1

def cardDiff(cards1, cards2):
    # cards1に含まれていてcards2に含まれていないカード
    return ((cards1 - cards2) > 0) * 1

def cardXor(cards1, cards2):
    # cards1かcards2どちらか一方にのみ含まれるカード
    return ((cards1 - cards2) != 0) * 1

def cardNot(cards):
    # cardsに含まれないカード
    return (cards == 0) * 1

