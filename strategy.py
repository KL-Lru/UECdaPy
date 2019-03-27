import numpy as np
from utils import *

def selectExchangeCards(cards, information):
    #-- 手札交換の選択アルゴリズム --

    # 弱い方から2枚選択
    quantity = information['exchange_quantity']
    work_table = np.zeros_like(cards)
    while quantity > 0:
        work_table += selectLowSingle( cardDiff(cards, work_table) )
        quantity -= 1

    return work_table
# end selectExchangeCards

def selectFlushCards(cards, information):
    #-- 場札なし非革命時の選択アルゴリズム --
    sequence_table, pair_table = makeTables(cards, information)

    # 階段優先で選択
    if existConstitution(sequence_table):
        for quantity in reversed(range(3,15)):
            n_table = nonNExclude(sequence_table, quantity)
            if existConstitution(n_table):
                return selectLowSequence(cards, n_table, information['have_joker'])

    # なければ組で選択
    if existConstitution(pair_table):
        for quantity in reversed(range(2,6)):
            n_table = nonNExclude(pair_table, quantity)
            if existConstitution(n_table):
                return selectLowPair(cards, n_table, joker_flag = information['have_joker'])

    # なければ単騎で選択
    return selectLowSingle(cards, information['have_joker'])
# end selectFlushCards

def selectFlushRevCards(cards, information):
    #-- 場札なし革命時の選択アルゴリズム --
    sequence_table, pair_table = makeTables(cards, information)

    # 階段優先で選択
    if existConstitution(sequence_table):
        for quantity in reversed(range(3,15)):
            n_table = nonNExclude(sequence_table, quantity)
            if existConstitution(n_table):
                return selectHighSequence(cards, n_table, information['have_joker'])

    # なければ組で選択
    if existConstitution(pair_table):
        for quantity in reversed(range(2,6)):
            n_table = nonNExclude(pair_table, quantity)
            if existConstitution(n_table):
                return selectHighPair(cards, n_table, joker_flag = information['have_joker'])

    # なければ単騎で選択
    return selectHighSingle(cards, information['have_joker'])

def selectFollowCards(cards, field, information):
    #-- 場札あり非革命時の選択アルゴリズム --
    field_info = parseFieldCards(field)
    filtered_cards = applyFilter(cards, field_info, information)
    sequence_table, pair_table = makeTables(filtered_cards, information)
    sequence_table[:, max(field_info['rank'])] = 0 # 階段ではJOKERを使う際に強さが場にあるカードと被り、提出できなくなるケースを防ぐため

    if field_info['type'] == 'sequence':
        n_table = nonNExclude(sequence_table, field_info['quantity']) 
        if existConstitution(n_table):
            return selectLowSequence(filtered_cards, n_table, joker_flag = information['have_joker'])
        return np.zeros_like(cards)

    if field_info['type'] == 'pair':
        n_table = nonNExclude(pair_table, field_info['quantity'])
        if existConstitution(n_table):
            if information['binded'] :
                return selectLowPair(filtered_cards, n_table, bind_suit = field_info['suit'], joker_flag = information['have_joker'])
            else:
                return selectLowPair(filtered_cards, n_table, joker_flag = information['have_joker'])
        return np.zeros_like(cards)

    # まだ提出されていないのなら場札は単騎
    # ペアになっているカードや階段を構成できるカードは除外しておく
    filtered_cards = cardDiff(filtered_cards, expandSequence(sequence_table))
    filtered_cards = cardDiff(filtered_cards, pair_table)

    return selectLowSingle(filtered_cards, joker_flag = information['have_joker'])
                

def selectFollowRevCards(cards, field, information):
    field_info = parseFieldCards(field)
    filtered_cards = applyRevFilter(cards, field_info, information)
    sequence_table, pair_table = makeTables(filtered_cards, information)
    sequence_table[:, min(field_info['rank'])] = 0 # 階段ではJOKERを使う際に強さが場にあるカードと被り、提出できなくなるケースを防ぐため

    if field_info['type'] == 'sequence':
        n_table = nonNExclude(sequence_table, field_info['quantity'])
        if existConstitution(n_table):
            return selectHighSequence(filtered_cards, n_table, joker_flag = information['have_joker'])
        return np.zeros_like(cards)

    if field_info['type'] == 'pair':
        n_table = nonNExclude(pair_table, field_info['quantity'])
        if existConstitution(n_table):
            if information['binded'] :
                return selectHighPair(filtered_cards, n_table, bind_suit = field_info['suit'], joker_flag = information['have_joker'])
            else:                            
                return selectHighPair(filtered_cards, n_table, joker_flag = information['have_joker'])
        return np.zeros_like(cards)

    # まだ提出されていないのなら場札は単騎
    # ペアになっているカードや階段を構成できるカードは除外しておく
    filtered_cards = cardDiff(filtered_cards, expandSequence(sequence_table))
    filtered_cards = cardDiff(filtered_cards, pair_table)
    return selectHighSingle(filtered_cards, joker_flag = information['have_joker'])

