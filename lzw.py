from lzwfile import LzwFile
import argparse


LZW_EXT = '.lzw'


def archive(args):
    file = args.file
    file_enc = file + LZW_EXT
    lzw = LzwFile(file)
    with open(file_enc, 'wb') as f:
        for b in lzw.encode():
            f.write(b)


def extract(args):
    file_enc = args.file
    file = file_enc[:-len(LZW_EXT)]
    lzw = LzwFile(file_enc)
    with open(file, 'wb') as f:
        for b in lzw.decode():
            f.write(b)


def parse_args():
    parser = argparse.ArgumentParser(description='LZW Archiver')
    parser.add_argument('file', type=str,
                        help='File you need to archive or extract')
    parser.add_argument('-x', default=False, help='Extract lzw archive',
                        action='store_true')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.x:
        extract(args)
    else:
        archive(args)
