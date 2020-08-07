from argparse import ArgumentParser

import spider


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-u', '--username', type=str)
    parser.add_argument('-p', '--password', type=str)
    parser.add_argument('-a', '--action', choices=['wish', 'comment'])
    return parser.parse_args()


def main():
    token = args.username, args.password
    s = spider.login_vpn(*token)
    spider.login_choose(*token, s)
    if args.action == 'wish':
        spider.get_wish(s)
    elif args.action == 'comment':
        spider.get_comment(s)
    else:
        assert 0


if __name__ == '__main__':
    args = parse_args()
    main()
