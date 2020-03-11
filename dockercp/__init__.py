import sys
import argparse
from .dockercopy import DEFAULT_BUFFER_SIZE, copy_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Source path of the file")
    parser.add_argument("destination", help="Destination path of the file")
    parser.add_argument("-b", "--buffer-length", default=DEFAULT_BUFFER_SIZE,
                        help="Size of the buffer used. Size is {} by default".format(DEFAULT_BUFFER_SIZE))
    args = parser.parse_args(None if sys.argv[2:] else ['-h'])
    copy_file(args.source, args.destination, int(args.buffer_length))


if __name__ == '__main__':
    main()
