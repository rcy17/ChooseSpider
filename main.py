from argparse import ArgumentParser

import spider


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-u", "--username", type=str)
    parser.add_argument("-p", "--password", type=str)
    parser.add_argument("-t", "--term", default="2021-2022-2", type=str)
    parser.add_argument("-v", "--webvpn", action="store_true")
    parser.add_argument("action", choices=["wish", "comment", "logout", "rest"])
    return parser.parse_args()


def main():
    token = args.username, args.password
    s = spider.login_vpn(*token, use_vpn=args.webvpn)
    urls = spider.WEBVPN_URL_DICT if args.webvpn else spider.NORMAL_URL_DICT
    spider.login_choose(*token, s, urls["login_choose"])
    if args.action == "wish":
        spider.get_wish(s, urls["wish"], args.term)
    elif args.action == "comment":
        spider.get_comment(s, urls["comment"], args.term)
    elif args.action == "logout":
        spider.logout_vpn()
    elif args.action == "rest":
        spider.get_rest(s, urls["rest"], args.term)
    else:
        assert 0


if __name__ == "__main__":
    args = parse_args()
    main()
