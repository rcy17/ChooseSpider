from requests import Session


def login_vpn(username, password, session: Session = None):
    if session is None:
        session = Session()

    data = {
        'auth_type': 'local',
        'username': username,
        'password': password,
        'sms_code': '',
    }
    session.post('https://webvpn.tsinghua.edu.cn/do-login?local_login=true', data=data)
    assert '首页' in session.get('https://webvpn.tsinghua.edu.cn/').text
    return session
