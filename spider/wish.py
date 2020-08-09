import json
import re
import time
from pathlib import Path
from datetime import datetime

from requests import Session
from tqdm import tqdm


def get_result(session, data):
    r = session.post('https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770'
                     'bc7b88b5c2d320506b1aec738590a49ba/xkBks.xkBksZytjb.do', data=data)
    total = int(re.search(r'共 (\d*) 页', r.text).group(1))
    result = []
    for page in tqdm(range(1, total + 1)):
        time.sleep(0.01)
        r = session.post('https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770'
                         'bc7b88b5c2d320506b1aec738590a49ba/xkBks.xkBksZytjb.do', data=data)
        data['page'] = page
        result += json.loads(re.search(r'var gridData = (\[.*?\]);', r.text, re.DOTALL).group(1))
    return result


def get_wish(session: Session):
    text = session.get('https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770'
                       'bc7b88b5c2d320506b1aec738590a49ba/xkBks.vxkBksXkbBs.do?m=xkqkSearch&p_xnxq=2020-2021-1').text
    current, then = re.findall(r'\d+年\d+月\d+日\d+时\d+分', text)
    data = {
        'm': 'tbzySearchBR',
        'page': 1,
        'p_xnxq': '2020-2021-1',
    }
    for m in ('tbzySearchBR', 'tbzySearchTy'):
        path = Path('data/' + m)
        path.mkdir(exist_ok=True, parents=True)
        file = path / (current + '.json')
        if file.exists():
            print(file, 'exists')
            continue
        data['m'], data['page'] = m, 1
        result = get_result(session, data)
        json.dump(result, open(file, 'w'), ensure_ascii=False)
    print('Next time:', then)
