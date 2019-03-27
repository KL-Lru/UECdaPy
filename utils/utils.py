import numpy as np

# Other utils -----

def qtyOfCards(cards):
    # JOKERのみ, "2"と記録されているためその分減らす
    return cards.sum() - (cards[4, 1] / 2) 

def existConstitution(cards):
    return not np.alltrue(cards == 0)

def expandSequence(sequence_table):
    work_table = np.zeros_like(sequence_table)
    for rank in range(15):
        for suit in range(4):
            qty = sequence_table[suit, rank]
            if qty > 0:
                for i in range(qty):
                    if rank + i >= 15:
                        break
                    work_table[suit, rank + i] = 1
    return work_table
    