
import os
import tarfile, io
from contextlib import closing

import docker

DEFAULT_BUFFER_SIZE = tarfile.RECORDSIZE


def copy_from_container(src, dst, buffer_size):
    container_name, container_path = src.split(":")
    container = docker.from_env().containers.get(container_name)
    tar_stream, tar_info = container.get_archive(container_path)
    tar_bytes = b''
    for bytestream in tar_stream:
        tar_bytes += bytestream
    tar = io.BytesIO(tar_bytes)
    archives = tarfile.open(fileobj=tar, mode='r|*', bufsize=buffer_size)
    with closing(archives) as tar_open:
        for item in tar_open:
            if os.path.isfile(dst):
                dst_path = dst
            else:
                dst_path = os.path.join(dst, item.name)
            with open(dst_path, 'wb') as dst_file:
                blocks, left = divmod(item.size, buffer_size)
                for block in range(blocks):
                    tarfile.copyfileobj(tar_open.fileobj, dst_file, buffer_size)
                if left > 0:
                    tarfile.copyfileobj(tar_open.fileobj, dst_file, left)


def copy_to_container(src, dst, buffer_size):
    container_name, dst_path = dst.split(":")
    container = docker.from_env().containers.get(container_name)
    tar = tarfile.open(mode="w|", fileobj=io.BytesIO(), bufsize=buffer_size)
    tar_info = tar.gettarinfo(name=src, arcname=os.path.basename(src))
    tar_header = tar_info.tobuf()
    tar.close()
    file_stat = os.stat(src)
    with open(src, 'rb', buffer_size) as file:
        padding_size = tarfile.BLOCKSIZE - (file_stat.st_size % tarfile.BLOCKSIZE)
        padding_size += 2 * tarfile.BLOCKSIZE
        padding = padding_size * tarfile.NUL
        bytes = b''
        bytes += tar_header
        bytes += file.read()
        bytes += padding
        byte_chain = io.BytesIO(bytes)
        container.put_archive(dst_path, byte_chain)
    tar.close()

def copy_file(src, dst, buffer_size):
    if ":" in src:
        if ":" in dst:
            raise UnhandledCaseError(
                "Cannot copy files from a container to another container. Copy {} to {}".format(src, dst))
        else:
            copy_from_container(src, dst, buffer_size)
    elif ":" in dst:
        copy_to_container(src, dst, buffer_size)
    else:
        raise UnhandledCaseError("Cannot copy files from host to host. Copy {} to {}".format(src, dst))


class UnhandledCaseError(Exception):
    """ Used for unexpected cases """
    pass

