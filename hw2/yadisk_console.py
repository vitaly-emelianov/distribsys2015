import argparse
import configparser
from yadisk_commands import *


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_ls = subparsers.add_parser('ls', help='shows all subdirectories and subfiles')
    parser_ls.add_argument('path', type=str)
    parser_ls.set_defaults(func=ls)

    parser_rm = subparsers.add_parser('rm', help='removes file or directory')
    parser_rm.add_argument('path', type=str)
    parser_rm.set_defaults(func=rm)

    parser_mv = subparsers.add_parser('mv', help='moves file or directory')
    parser_mv.add_argument('path', type=str)
    parser_mv.add_argument('destination', type=str)
    parser_mv.set_defaults(func=mv)

    parser_cp = subparsers.add_parser('cp', help='copies file or directory')
    parser_cp.add_argument('path', type=str)
    parser_cp.add_argument('destination', type=str)
    parser_cp.set_defaults(func=cp)

    parser_upload = subparsers.add_parser('upload', help='uploads file to yandex disk')
    parser_upload.add_argument('local_path', type=str)
    parser_upload.add_argument('path', type=str)
    parser_upload.set_defaults(func=upload)

    parser_download = subparsers.add_parser('download', help='downloads file from yandex disk')
    parser_download.add_argument('path', type=str)
    parser_download.add_argument('local_path', type=str)
    parser_download.set_defaults(func=download)

    args = parser.parse_args()
    args.func(args)
