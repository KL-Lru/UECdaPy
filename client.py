from connection import connect
from strategy import *
import numpy as np

class Client(object):
    def __init__(self, name = 'default'):
        self.name   = name
        self.hands  = np.empty((5,15), dtype = int)
        self.field  = np.empty((5,15), dtype = int)
        self.submit = np.empty((5,15), dtype = int)
        self.info   = {}

    def exchangeCard(self, hands, info):
        # 交換するカードを選択する
        # 大富豪, 富豪の時のみ各ゲーム開始時に呼び出される

        self.hands[...] = hands
        self.info = info
        self.submit.fill(0)

        self.submit[...] = selectExchangeCards(hands, info)

        return self.submit

    def submitCard(self, hands, info):
        # 提出するカードを選択する
        # 自分が提出する番にのみ呼び出される

        self.hands[...] = hands
        self.info       = info
        self.submit.fill(0)

        if info['flushed']:
            if not info['revoluted']:
                self.submit[...] = selectFlushCards(hands, info)
            else:
                self.submit[...] = selectFlushRevCards(hands, info)

        else:
            if not info['revoluted']:
                self.submit[...] = selectFollowCards(hands, self.field, info)
            else:
                self.submit[...] = selectFollowRevCards(hands, self.field, info)
        return self.submit

    def updateField(self, field, info):
        # 場の情報を更新する
        # プレイヤ(自分以外を含む)がカードを提出する前に呼び出される
        
        self.field[...] = field
        self.info       = info

    def getName(self):
        # サーバに送信する名前を返す
        return self.name
    
    def setIndex(self, index):
        # サーバから自分のプレイヤidを受け取る
        self.index = index

if __name__ == '__main__':
    client = Client('default')
    connect(client)