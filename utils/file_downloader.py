# --*-- coding:utf-8 --*--

from urllib.request import urlretrieve
from tqdm import tqdm
from config import *


class TqdmUpTo(tqdm):

    last_block = 0

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update((b - self.last_block) * bsize)
        self.last_block = b


class Downloader(object):
    def __init__(self, file_link):
        self.file_link = file_link

    def download(self):
        file = SOURCE_IPS_PATH
        with TqdmUpTo(
                unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                desc=file
        ) as t:
            urlretrieve(
                self.file_link, filename=file, reporthook=t.update_to,
                data=None
            )

