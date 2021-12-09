import csv
import json
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-e", "--encoding", default="GBK", type=str)
    parser.add_argument("in_file", type=str)
    parser.add_argument("out_file", type=str)
    parser.add_argument("headers", nargs="+", type=str)
    return parser.parse_args()


def json2csv(in_file, out_file, headers, encoding):
    data = json.load(open(in_file, encoding=encoding))
    with open(out_file, "w", encoding=encoding, newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)
        writer.writerows(data)


def main():
    args = parse_args()
    json2csv(args.in_file, args.out_file, args.headers, args.encoding)


if __name__ == "__main__":
    main()
