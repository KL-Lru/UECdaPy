def parseInformation(table):
    info = {}
    info['have_joker']        = (table[4, 1] > 0)
    info['exchange_quantity'] = table[5, 1]
    info['active_player']     = table[5, 3]
    info['flushed']           = bool(table[5, 4])
    info['revoluted']         = bool(table[5, 6])
    info['binded']            = bool(table[5, 7])
    info['remain'] = {}
    info['class']  = {}
    info['seat']   = {}
    for i in range(5):
        info['remain'][i] = table[6, i]
        info['class'][i]  = table[6, i+5]
        info['seat'][i]   = table[6, i+10]
    return info

def parseFieldCards(field):
    info = {}
    field_suit = set()
    field_rank = set()

    for suit in range(4):
        for rank in range(15)[::-1]:
            if field[suit, rank] > 0:
                field_suit.add(suit)
                field_rank.add(rank)

    info['suit']      = list(field_suit)
    info['rank']      = list(field_rank)
    info['quantity']  = max(len(field_suit), len(field_rank))
    
    if len(info['rank']) > 1:
        info['type'] = 'sequence'
    elif len(info['suit']) > 1:
        info['type'] = 'pair'
    elif len(info['suit']) == 1 and len(info['rank']) == 1:
        info['type'] = 'single'
    else:
        info['type'] = 'none'
    return info
    