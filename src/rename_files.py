""" Script to rename files """

import unidecode
import os

DATAPATH = '../data/raw/'

def rename_files():
    files = os.listdir(DATAPATH)
    for file_src in files:
        file_dst = '_'.join(unidecode.unidecode(file_src.replace('-', '').lower()).split(' '))
        os.rename(os.path.join('../data/raw/', file_src), os.path.join('../data/raw/', file_dst))


if __name__='__main__':
    rename_files()

