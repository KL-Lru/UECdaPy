# カード行列同士の論理演算関数群

def cardOr(cards1, cards2):
    """
    cards1とcards2のどちらかに含まれているカードを計算する

    Parameters
    ----------
    cards1, cards2: np.array((5,15))
        手札や場札を示す配列
    
    Return
    ------
    np.array((5,15))
    cards1とcards2のどちらかに含まれているカードを示す配列
    """
    return ((cards1 + cards2) > 0) * 1

def cardAnd(cards1, cards2):
    """
    cards1とcards2のどちらにも含まれているカードを計算する

    Parameters
    ----------
    cards1, cards2: np.array((5,15))
        手札や場札を示す配列
    
    Return
    ------
    np.array((5,15))
    cards1とcards2のどちらにも含まれているカードを示す配列
    """
    return ((cards1 * cards2) > 0) * 1

def cardDiff(cards1, cards2):
    """
    cards1に含まれていてcards2に含まれていないカードを計算する

    Parameters
    ----------
    cards1, cards2: np.array((5,15))
        手札や場札を示す配列
    
    Return
    ------
    np.array((5,15))
    cards1に含まれていてcards2に含まれていないカードを示す配列
    """
    return ((cards1 - cards2) > 0) * 1

def cardXor(cards1, cards2):
    """
    cards1かcards2どちらか一方にのみ含まれるカードを計算する

    Parameters
    ----------
    cards1, cards2: np.array((5,15))
        手札や場札を示す配列
    
    Return
    ------
    np.array((5,15))
    cards1かcards2どちらか一方にのみ含まれるカードを示す配列
    """
    return ((cards1 - cards2) != 0) * 1

def cardNot(cards):
    """
    cardsに含まれないカードを計算する

    Parameters
    ----------
    cards: np.array((5,15))
        手札や場札を示す配列
    
    Return
    ------
    np.array((5,15))
    cardsに含まれないカードを示す配列
    """
    return (cards == 0) * 1

