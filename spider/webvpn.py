import json
from datetime import datetime
from pathlib import Path
import re

from requests import Session


def logout_vpn():
    path = Path(".cache")
    if not path.exists():
        return
    for file in path.iterdir():
        if file.is_file():
            file.unlink()


def login_vpn(username, password, session: Session = None, use_vpn=True):
    def check_error():
        text = session.get("https://webvpn.tsinghua.edu.cn/").text
        if "注销" not in text:
            return text

    if not use_vpn:
        return Session()

    path = Path(".cache")
    file = path / "cookies.json"
    path.mkdir(exist_ok=True)
    if session is None:
        session = Session()

    if file.exists():
        # a shortcut
        cookies = json.load(open(file))
        session.cookies.update(cookies)
        if not check_error():
            print("Cache for webvpn is valid")
            return session
        print("Cache for webvpn is invalid")
        file.unlink()
        session = Session()

    data = {
        "auth_type": "local",
        "username": username,
        "password": password,
        "sms_code": "",
    }
    session.post("https://webvpn.tsinghua.edu.cn/do-login?local_login=true", data=data)
    path = Path(".log")
    path.mkdir(exist_ok=True)
    error = check_error()
    if error:
        with open(
            str(path / datetime.now().strftime("%Y%m%d%H%M%S.html")),
            "w",
            encoding="utf-8",
        ) as file:
            file.write(error)
        raise AssertionError(f"登录失败")
    cookies = session.cookies.get_dict()
    json.dump(cookies, open(file, "w"), ensure_ascii=False)
    return session
