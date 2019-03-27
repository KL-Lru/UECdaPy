import numpy as np

# Filters -----
# フィルタ適応する
def applyFilter(cards, field_info, info):
    # 提出出来ないカードを除外する
    filtered_cards = lowExclude(cards, max(field_info['rank']))
    if info['binded']:
        filtered_cards = lockOnly(filtered_cards, field_info['suit'])
    return filtered_cards

def applyRevFilter(cards, field_info, info):
    # 提出出来ないカードを除外する(革命時用)
    filtered_cards = highExclude(cards, min(field_info['rank']))
    if info['binded']:
        filtered_cards = lockOnly(filtered_cards, field_info['suit'])
    return filtered_cards

# By rank ---
def lowExclude(cards, rank):
    # rank以下のカードを除外する
    filtered_table = np.array(cards, dtype = int)
    filtered_table[:, :rank+1] = 0
    return filtered_table

def highExclude(cards, rank):
    # rank以上のカードを除外する
    filtered_table = np.array(cards, dtype = int)
    filtered_table[:, rank:] = 0
    return filtered_table

# By value ---
def nonNExclude(cards, n):
    # 値がn以外の物を除外する
    return (cards == n) * n

def lessNExclude(cards, n):
    # 値がn未満のカードを除外し、n以上の物をnにする
    return (cards >= n) * n

# By suit ---
def lockOnly(cards, suit):
    # suit以外のカードを除外する
    filtered_table = np.zeros_like(cards, dtype = int)
    filtered_table[suit, :] = cards[suit, :]
    return filtered_table

