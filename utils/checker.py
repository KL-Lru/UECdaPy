import numpy as np

def existConstitution(table):
    """
    可能な構成が存在しているかを判定する

    Parameter
    ---------
    table: np.array((5,15))
        組や階段の構成を示す配列

    Return
    ------
    bool
        構成が一つでもあればTrue, なければFalse
    """
    return not np.alltrue(table == 0)

