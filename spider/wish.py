import json
import re
import time
from pathlib import Path
from datetime import datetime

from requests import Session
from tqdm import tqdm


def get_result(session, data, url):
    r = session.post(url, data=data)
    total = int(re.search(r"共 (\d*) 页", r.text).group(1))
    result = []
    for page in tqdm(range(1, total + 1)):
        time.sleep(0.01)
        r = session.post(url, data=data)
        data["page"] = page
        try:
            result += json.loads(
                re.search(
                    r"var gridData = (\[.*?\]);", r.text.replace("\n", ""), re.DOTALL
                ).group(1)
            )
        except:
            print(r.text)
            open("error.txt", "w").write(
                re.search(r"var gridData = (\[.*?\]);", r.text, re.DOTALL).group(1)
            )
    return result


def spider_run(session, data, current, url):
    m = data["m"]
    path = Path("data/" + m)
    path.mkdir(exist_ok=True, parents=True)
    file = path / (current + ".json")
    if file.exists():
        print(file, "exists")
        return
    result = get_result(session, data, url)
    return result, file


def get_wish(session: Session, urls, term):
    text = session.get(
        f"https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770"
        f"bc7b88b5c2d320506b1aec738590a49ba/xkBks.vxkBksXkbBs.do?m=xkqkSearch&p_xnxq={term}"
    ).text
    times = re.findall(r"\d+年\d+月\d+日\d+时\d+分", text)
    if not times:
        times = ["抽签结果"]
    len(times) == 2 or times.append(None)
    current, then = times
    data = {
        "m": "tbzySearchBR",
        "page": 1,
        "p_xnxq": term,
    }
    url = (
        "https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770"
        "bc7b88b5c2d320506b1aec738590a49ba/xkBks.xkBksZytjb.do"
    )
    for m in ("tbzySearchBR", "tbzySearchTy"):
        data["m"] = m
        result, file = spider_run(session, data, current, url)
        json.dump(result, open(file, "w", encoding="utf-8"), ensure_ascii=False)
    if then:
        print("Next time:", then)


def get_queue(session: Session, result, limit, offset, urls, term):
    data = {
        "m": "selectBksDlCount",
        "kc_message": ";".join(
            f"{term}_{each[0]}_{each[1]}" for each in result[offset : offset + limit]
        ),
    }
    url = urls["queue"]
    if not limit:
        return []
    r = session.post(url, data=data)
    return r.json()


def get_rest(session: Session, urls, term):
    data = {
        "m": "kylSearch",
        "page": 1,
        "p_xnxq": term,
    }
    url = urls["rest"]
    result, file = spider_run(
        session, data, datetime.now().strftime(f"{term}-%Y年%m月%d日%H时%M分"), url
    )
    page_size = 20
    total = len(result)
    queue = []
    for page in tqdm(range(total // page_size)):
        queue += get_queue(session, result, page_size, page * page_size, urls, term)
    finished = page_size * (total // page_size)
    queue += get_queue(session, result, total - finished, finished, urls, term)
    for l, q in zip(result, queue):
        l.insert(5, q.get("dlrs", ""))
    json.dump(result, open(file, "w", encoding="utf-8"), ensure_ascii=False)
