# 配列から情報をわかりやすく格納する関数群

def parseInformation(table):
    """
    サーバから送られてきた情報をparseする

    Parameter
    ---------
    table: np.array((8,15))
        サーバから送られてくる配列

    Return
    ------
    info: dict
        サーバから通知された情報を格納したdict
        have_joker: bool
            JOKERを持っているか否か
        exchange_quantity: int
            ゲーム開始時に交換する必要のある枚数
        active_player: int
            現在提出する番のプレイヤ番号
        flushed: bool
            場が流れた直後か否か
        revoluted: bool
            革命状態か否か
        binded: bool
            縛り状態か否か
        remain: list(int)
            各プレイヤの残り手札枚数
        class: list(int)
            各プレイヤの役職
        seat: list(int)
            各プレイヤが座っている席番号
    """
    info = {}
    info['have_joker']        = (table[4, 1] > 0)
    info['exchange_quantity'] = table[5, 1]
    info['active_player']     = table[5, 3]
    info['flushed']           = bool(table[5, 4])
    info['revoluted']         = bool(table[5, 6])
    info['binded']            = bool(table[5, 7])
    info['remain'] = []
    info['class']  = []
    info['seat']   = []
    for i in range(5):
        info['remain'].append(table[6, i])
        info['class'].append(table[6, i+5])
        info['seat'].append(table[6, i+10])
    return info

def parseFieldCards(field):
    """
    場の情報をparseする

    Parameter
    ---------
    field: np.array((5,15))
        場札を示す配列

    Return
    ------
    info: dict
        場の情報を格納したdict
        suit: list(int)
            場札の絵柄
        rank: list(int)
            場札の強さ
        quantity: int
            場札の構成枚数
        type: str
            場札の構成種別
            sequence -> 階段
            pair     -> 組
            single   -> 単騎
            none     -> 場札なし
    """
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
    elif info['quantity'] == 1:
        info['type'] = 'single'
    else:
        info['type'] = 'none'
    return info
    