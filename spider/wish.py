import json
import re
import time
from pathlib import Path
from datetime import datetime

from requests import Session
from tqdm import tqdm


def get_result(session, data, url):
    r = session.post(url, data=data)
    total = int(re.search(r'共 (\d*) 页', r.text).group(1))
    result = []
    for page in tqdm(range(1, total + 1)):
        time.sleep(0.01)
        r = session.post(url, data=data)
        data['page'] = page
        try:
            result += json.loads(re.search(r'var gridData = (\[.*?\]);', r.text.replace('\n', ''), re.DOTALL).group(1))
        except:
            print(r.text)
            open('error.txt', 'w').write(re.search(r'var gridData = (\[.*?\]);', r.text, re.DOTALL).group(1))
    return result

def spider_run(session, data, current, url):
    m = data['m']
    path = Path('data/' + m)
    path.mkdir(exist_ok=True, parents=True)
    file = path / (current + '.json')
    if file.exists():
        print(file, 'exists')
        return
    result = get_result(session, data, url)
    json.dump(result, open(file, 'w'), ensure_ascii=False)



def get_wish(session: Session):
    text = session.get('https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770'
                       'bc7b88b5c2d320506b1aec738590a49ba/xkBks.vxkBksXkbBs.do?m=xkqkSearch&p_xnxq=2020-2021-1').text
    times = re.findall(r'\d+年\d+月\d+日\d+时\d+分', text)
    if not times:
        times = ['抽签结果']
    len(times) == 2 or times.append(None)
    current, then = times
    data = {
        'm': 'tbzySearchBR',
        'page': 1,
        'p_xnxq': '2020-2021-1',
    }
    url = 'https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770' \
          'bc7b88b5c2d320506b1aec738590a49ba/xkBks.xkBksZytjb.do'
    for m in ('tbzySearchBR', 'tbzySearchTy'):
        data['m'] = m
        spider_run(session, data, current, url)
    if  then:
        print('Next time:', then)


def get_rest(session: Session):
    data = {
        'm': 'kylSearch',
        'page': 1,
        'p_xnxq': '2020-2021-1',
    }
    url = 'https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770' \
          'bc7b88b5c2d320506b1aec738590a49ba/xkBks.vxkBksJxjhBs.do'
    spider_run(session, data, datetime.now().strftime('%Y年%m月%d日%H时%M分'), url)
