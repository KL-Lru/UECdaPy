import numpy as np

# Selectors -----
# 全て基礎となるBase関数とそれを呼び出すだけのHelper関数から成っています

# Sequence ---
# Base --
def selectBaseSequence(cards, sequence_table, scope):
    # 手札(cards)と階段構成テーブル(sequence_table)から提出可能な手を構成する
    # 役の強さはカードを置ける範囲(scope)の並び順に依存する
    one_seq_table = np.zeros_like(cards, dtype = int)

    for rank in scope:
        for suit in range(4):
            if sequence_table[suit, rank] > 0:
                for con_num in range(sequence_table[suit, rank]): 
                    if cards[suit, rank + con_num] == 1:
                        one_seq_table[suit, rank + con_num] = 1
                    else: # なければjokerを使う(Sequenceなので足りないならJOKERを使っていると判定して大丈夫)
                        one_seq_table[suit, rank + con_num] = 2
                return one_seq_table
    return one_seq_table

# Helper --
def selectLowSequence(cards, sequence_table, joker_flag = False):
    return selectBaseSequence(cards, sequence_table, range(15))

def selectHighSequence(cards, sequence_table, joker_flag = False):
    return selectBaseSequence(cards, sequence_table, reversed(range(15)))

# Pair ---
# Base --
def selectBasePair(cards, pair_table, subsutitute, scope, bind_suit):
    # 手札(cards)と組構成テーブル(pair_table)から提出可能な手を構成する
    # 役の強さはカードを置ける範囲(scope)の並び順に依存する
    # 置換対象(substitute)はJOKERを使用する時のみ2と入力し, 使用しない場合は0を入力する
    # 縛り絵柄(bind_suit)は必要に応じて指定する(Filterと併用していればJOKERを使う時以外は使わない)
    one_pair_table = np.zeros_like(cards, dtype = int)

    for rank in scope:
        for suit in range(4):
            if pair_table[suit, rank] > 0:
                set_sub = False
                set_cnt = 0
                quantity = pair_table[suit, rank]
                for con_suit in range(5):
                    if set_cnt == quantity: break
                    if con_suit not in bind_suit: continue  
                                          
                    if cards[con_suit, rank] == 1:
                        one_pair_table[con_suit, rank] = 1
                        set_cnt += 1
                    elif not set_sub:
                        one_pair_table[con_suit, rank] = subsutitute
                        set_cnt += 1 if subsutitute == 2 else 0
                        set_sub = True
                return one_pair_table
    return one_pair_table

# Helper --
def selectLowPair(cards, pair_table, bind_suit = range(5), joker_flag = False):
    return selectBasePair(cards, pair_table, 2 if joker_flag else 0, range(15), bind_suit = bind_suit)

def selectHighPair(cards, pair_table, bind_suit = range(5), joker_flag = False):
    return selectBasePair(cards, pair_table, 2 if joker_flag else 0, reversed(range(15)), bind_suit = bind_suit)

# Single ---
def selectBaseSingle(cards, subsutitute, scope):
    # 手札(cards)から提出可能な手を構成する
    # 役の強さはカードを置ける範囲(scope)の並び順に依存する
    # 置換対象(substitute)はJOKERを使用する時のみ2と入力し, 使用しない場合は0を入力する
    single_table = np.zeros_like(cards, dtype = int)

    for rank in scope:
        for suit in range(4):
            if cards[suit, rank] > 0:
                single_table[suit, rank] = 1
                return single_table

    # まだreturnされていないならJOKERか0を入れて返す
    single_table[0,14] = subsutitute
    return single_table

def selectLowSingle(cards, joker_flag = False):
    return selectBaseSingle(cards, 2 if joker_flag else 0, range(15))

def selectHighSingle(cards, joker_flag = False):
    return selectBaseSingle(cards, 2 if joker_flag else 0, reversed(range(15)))
