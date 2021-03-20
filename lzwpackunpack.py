import six
import struct


class LzwPackUnpack:
    @staticmethod
    def pack(codes_iter):
        current_table_size = 256
        min_length = 8
        current_length = min_length
        remain_bits = []

        for code in codes_iter:

            newbits = LzwPackUnpack.int_to_bits(code, current_length)
            remain_bits = remain_bits + newbits

            current_table_size += 1

            if current_table_size >= (2 ** current_length):
                current_length += 1

            while len(remain_bits) > 8:
                bits_to_become_bytes = remain_bits[:8]
                nextbytes = LzwPackUnpack.bits_to_bytes(bits_to_become_bytes)
                for byte in nextbytes:
                    yield struct.pack("B", byte)

                remain_bits = remain_bits[8:]

        if remain_bits:
            remain_bytes = LzwPackUnpack.bits_to_bytes(remain_bits)
            for byte in remain_bytes:
                yield struct.pack("B", byte)

    @staticmethod
    def unpack(bytes_iter):
        current_table_size = 256
        min_length = 8
        current_length = min_length
        bits = []

        for bit in LzwPackUnpack.bytes_to_bits(bytes_iter):
            bits.append(bit)

            if len(bits) == current_length:
                code = LzwPackUnpack.bits_to_int(bits)
                bits = []
                current_table_size += 1
                while current_table_size >= (2 ** current_length):
                    current_length += 1

                yield code

    @staticmethod
    def bits_to_bytes(bits):
        ret = []
        nextbyte = 0
        nextbit = 7
        for bit in bits:
            if bit:
                nextbyte = nextbyte | (1 << nextbit)

            if nextbit:
                nextbit = nextbit - 1
            else:
                ret.append(nextbyte)
                nextbit = 7
                nextbyte = 0

        if nextbit < 7:
            ret.append(nextbyte)
        return ret

    @staticmethod
    def bytes_to_bits(bytesource):
        for b in bytesource:
            value = six.byte2int(b)

            for bitplusone in range(8, 0, -1):
                bitindex = bitplusone - 1
                nextbit = 1 & (value >> bitindex)
                yield nextbit

    @staticmethod
    def int_to_bits(number, width=None):
        remains = number
        retreverse = []
        while remains:
            retreverse.append(remains & 1)
            remains = remains >> 1

        retreverse.reverse()

        return_value = retreverse
        if width is not None:
            ret_head = [0] * (width - len(return_value))
            return_value = ret_head + return_value

        return return_value

    @staticmethod
    def bits_to_int(bits):
        return_value = 0
        lsb_first = [b for b in bits]
        lsb_first.reverse()

        for bit_index in range(len(lsb_first)):
            if lsb_first[bit_index]:
                return_value = return_value | (1 << bit_index)

        return return_value