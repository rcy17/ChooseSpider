from io import BytesIO

from requests import Session
from PIL import Image


def login_choose(username, password, session: Session):
    session.get('https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b265377'
                '0bc7b88b5c2d320506b1aec738590a49ba/xklogin.do')
    Image.open(BytesIO(session.get('https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b'
                                   '3f3b2653770bc7b88b5c2d320506b1aec738590a49ba/login-jcaptcah.jpg?vpn-1&'
                                   'captchaflag=login1').content)).show()
    code = input('Please input validate code:')
    data = {
        'j_username': username,
        'j_password': password,
        'captchaflag': 'login1',
        '_login_image_': code,
    }
    r = session.post('https://webvpn.tsinghua.edu.cn/https-443/77726476706e69737468656265737421eaff4b8b3f3b2653770bc7b8'
                     '8b5c2d320506b1aec738590a49ba/j_acegi_formlogin_xsxk.do', data=data)
    if '本科生选课' not in r.text:
        print('登录失败，请重试')
        return login_choose(username, password, session)
    return session