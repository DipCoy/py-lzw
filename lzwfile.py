import os
import six
import os_extensions as os_ext
from lzwpackunpack import LzwPackUnpack


class LzwFile:
    def __init__(self, paths):
        self._table = LzwFile._get_lzw_encode_start_table()
        self._decode_table = LzwFile._get_lzw_decode_start_table()
        if isinstance(paths, str):
            self._paths = [paths]
            if not os.path.exists(paths):
                raise FileNotFoundError(paths)
            return

        if isinstance(paths, list):
            self._paths = paths
            if not all(os.path.exists(path) for path in paths):
                not_found_paths = filter(lambda path: not os.path.exists(path),
                                         paths)
                raise FileNotFoundError(not_found_paths)
            return

        raise ValueError(f'{type(paths)} type is not appropriate')

    def add_code(self, byte_string):
        self._table[byte_string] = len(self._table)

    @staticmethod
    def _get_lzw_encode_start_table():
        table = dict()
        for number in range(256):
            table[bytes(number.to_bytes(1, 'big'))] = number

        return table

    @staticmethod
    def _get_lzw_decode_start_table():
        table = dict()
        for number in range(256):
            table[number] = six.int2byte(number)

        return table

    def encode(self, path_to_file=None):
        codes_iter = self.get_codes_from_bytes(
            os_ext.read_byte_by_byte(self._paths[0]))
        return LzwPackUnpack.pack(codes_iter)

    def get_codes_from_bytes(self, bytes_iter):
        # -> [1, 2, 257, 23]
        string = b''
        for byte in bytes_iter:
            string_plus_byte = string + byte
            if string_plus_byte in self._table:
                string = string_plus_byte
            else:
                self.add_code(string_plus_byte)
                yield self._table[string]
                string = byte
        if string in self._table:
            yield self._table[string]

    def decode(self, path_to_archive=None):
        bytes_iter = os_ext.read_byte_by_byte(self._paths[0])
        codes_iter = LzwPackUnpack.unpack(bytes_iter)
        return self.decode_codes(codes_iter)

    def decode_codes(self, codes_iter):
        prefix = None
        for code in codes_iter:
            if code in self._decode_table:
                byte_to_return = self._decode_table[code]
                if prefix is not None:
                    self._decode_table[len(self._decode_table)] = \
                        prefix + \
                        six.int2byte(six.indexbytes(byte_to_return, 0))

            else:
                byte_to_return = prefix + \
                                 six.int2byte(six.indexbytes(prefix, 0))
                self._decode_table[len(self._decode_table)] = byte_to_return
            prefix = byte_to_return

            yield byte_to_return
