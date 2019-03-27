import socket
from struct import Struct
from utils import parseInformation
import numpy as np

# Struct --------------------
integer_struct = Struct('!1I')
table_struct   = Struct('!120I')

# Global Variable -----------
sock = None

def connect(client, host = '127.0.0.1', port = 42485):
    """
    クライアントをサーバに接続する

    Parameters
    ----------
    client: Client
        client.pyに定義される最低限のメソッドを備えたクラスインスタンス
    host: str '127.0.0.1'
        接続先のipアドレス
    port: int 42485
        接続先のポート番号
    """

    global sock
    # socket設定
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    try:
        # 初期化
        field  = np.zeros((5,15), dtype = int)
        hand   = np.zeros((5,15), dtype = int)
        submit = np.zeros((8,15), dtype = int)

        game_state = 0

        # クライアント名の送信
        sendName(client.getName())

        index = recvInt()
        client.setIndex(index)
        print(index)
        while not finishAllGame(game_state):
            game_state = 0

            recv = recvTable()
            if canExchange(recv):
                # 手札交換する順位であれば交換する
                hand[...] = recv[:5, :]
                info = parseInformation(recv)

                submit[:5, ...] = client.exchangeCard(hand, info)
                sendTable(submit)

            while not finishOneGame(game_state):
                recv = recvTable()
                info = parseInformation(recv)

                client.updateField(field, info)
                
                if canSubmit(recv):
                    # 自分の提出順であれば提出する
                    hand[...] = recv[:5, :]
                    tmp = client.submitCard(hand, info)
                    submit[:5, ...] = tmp

                    sendTable(submit)
                    accept = recvInt()
                    """
                    # for debug
                    if accept != 9 and not np.alltrue(submit == 0):
                        print('Not Accepted. ')
                        print('info')
                        print(' rev? : ' + str(info['revoluted']))
                        print(' binded? : ' + str(info['binded']))
                        print(' flushed? : ' + str(info['flushed']))
                        print(' have_joker? : ' + str(info['have_joker']))
                        print('hand')
                        print(hand)
                        print('field')
                        print(field)
                        print('submit')
                        print(submit)
                    """
                recv = recvTable()
                field[...] = recv[:5, :]

                game_state = recvInt()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        raise

def recvInt():
    """
    接続先から整数値1つを受け取る

    Returns
    -------
    受け取った整数値
    """
    global sock
    recv = sock.recv(4)
    unpacked_data = integer_struct.unpack(recv)
    return unpacked_data[0]

def recvTable():
    """
    接続先から8行15列テーブルを受け取る

    Returns
    -------
    受け取った8行15列テーブル
    """
    global sock
    recv = sock.recv(480)
    unpacked_data = table_struct.unpack(recv)
    recv_data     = np.reshape(unpacked_data,(8,15))
    return recv_data

def sendName(name, protocol = 20070):
    """
    接続先へクライアントの名前とプロトコルを送信する

    Parameters
    ----------
    name: str
        クライアントの名前
    protocol: int 20070
        使用するプロトコルのversion
    """

    send_data = np.zeros((8,15), dtype = int)
    send_data[0, 0] = protocol
    for i, c in enumerate(name):
        send_data[1, i] = ord(c)
    sendTable(send_data)

def sendTable(table):
    """
    接続先へ8行15列テーブルを送信する

    Parameters
    ----------
    table: np.ndarray
        送信するテーブル
    """

    global sock
    send_table = np.resize(table, 120)
    send_list = send_table.tolist()
    sock.sendall( table_struct.pack(*send_list) )


def finishAllGame(game_state):
    """
    全ゲームが終了したか判定する

    Parameters
    ----------
    game_state: int
        ゲームの状態フラグ
    """
    return game_state == 2

def finishOneGame(game_state):
    """
    1ゲームが終了したか判定する

    Parameters
    ----------
    game_state: int
        ゲームの状態フラグ
    """
    return game_state > 0

def canExchange(table):
    """
    カード交換で選ぶことが可能か判定する

    Parameter
    ---------
    table: np.array((8,15))
        サーバから送られてくる配列
    """
    return table[5][1] > 0

def canSubmit(table):
    """
    カード提出が可能か判定する

    Parameter
    ---------
    table: np.array((8,15))
        サーバから送られてくる配列
    """
    return table[5][2] > 0

