from io import BytesIO
from pathlib import Path

from requests import Session
from PIL import Image


def login_choose(username, password, session: Session, urls: dict):
    r = session.get(urls["main"])
    if "本科生选课" in r.text:
        # shortcut
        print("cache for choose is valid")
        return session

    session.get(urls["login_page"])
    image = Image.open(BytesIO(session.get(urls["login_image"]).content))
    assert isinstance(image, Image.Image)
    image.show()
    path = Path(".cache")
    path.mkdir(exist_ok=True)
    image.save(str(path / "code.jpg"))
    code = input("Please input validate code:").strip().upper()
    data = {
        "j_username": username,
        "j_password": password,
        "captchaflag": "login1",
        "_login_image_": code,
    }
    r = session.post(
        urls["login_post"],
        data=data,
    )
    if "本科生选课" not in r.text:
        print("登录失败，请重试")
        return login_choose(username, password, session, urls)
    return session
