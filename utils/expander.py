import numpy as np

def expandSequence(sequence_table):
    """
    階段構成テーブルから階段に使用可能なカードを展開する

    Parameter
    ---------
    sequence_table: np.array((5,15))
        階段の構成を示す配列

    Return
    ------
    work_table: np.array((5,15))
        構成に使用可能なカード全てを列挙した配列
    """
    work_table = np.zeros_like(sequence_table)
    for rank in range(15):
        for suit in range(4):
            quantity = sequence_table[suit, rank]
            if quantity > 0:
                for i in range(quantity):
                    if rank + i >= 15:
                        break
                    work_table[suit, rank + i] = 1
    return work_table

def expandPair(pair_table):
    """
    組構成テーブルから組に使用可能なカードを展開する

    Parameter
    ---------
    pair_table: np.array((5,15))
        組の構成を示す配列

    Return
    ------
    work_table: np.array((5,15))
        構成に使用可能なカード全てを列挙した配列
    """
    work_table = (pair_table != 0) * 1
    return work_table
    