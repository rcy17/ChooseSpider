from json import loads
from pathlib import Path
from datetime import datetime

from requests import Session
from openpyxl import Workbook


def get_comment(session: Session, urls, term):
    data = {
        "page": 1,
        "rows": 20,
    }
    r = session.post(
        "https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770bc7b"
        "88b5c2d320506b1aec738590a49ba/xkBks.xgpg_xspjyxkt.do?vpn-12-o1-zhjwxk.cic.tsinghua.edu.cn&"
        f"cm=xgpg_qbkcmycdzbData&p_xnxq={term}&p_xslb=bks",
        data=data,
    )
    assert r.status_code == 200
    data = loads(r.content.decode("gbk"))
    wb = Workbook()
    ws = wb.active
    ws.append(
        "开课院系 | 教师名 | 课程号 | 课程名 | 分数1 | 分数2 | 分数3 | 分数4 | 分数5 | 分数6 | 分数7".split(" | ")
    )
    key_order = "kkdwmc jsm kch kcm fs1 fs2 fs3 fs4 fs5 fs6 fs7".split()
    for row in data["rows"]:
        ws.append(tuple(row[k] for k in key_order))
    path = Path("data/comment")
    path.mkdir(exist_ok=True)
    wb.save(str(path / datetime.now().strftime("%Y%m%d%H%M%S.xlsx")))
