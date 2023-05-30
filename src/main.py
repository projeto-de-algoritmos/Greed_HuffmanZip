from huffman import *
import sys


def usage():
    print('USAGE:')
    print('python3 main.py [COMMAND] <path>\n')
    print('COMMANDS:')
    print('-c, -C: Compress archive')
    print('-x, -X: Decompress archive')

def main():
    try:
        if sys.argv[1] == '-C' or sys.argv[1] == '-c':
            archive = sys.argv[2]
            with open(archive, 'rb') as fin:
                data = fin.read()
                compressed_bits, codes, probabilities = compress(data)
                write_codes(codes, probabilities)
                write_compressed_file(compressed_bits, codes, f'{archive}.bin')
        elif sys.argv[1] == '-x' or sys.argv[1] == '-X':
            archive = sys.argv[2]
            data = decompress(archive)
            new_file_name = archive.split('.')
            new_file_name = ''.join(new_file_name[:-2]) + '_decompressed.' + new_file_name[-2]
            write_decompressed_data(data, new_file_name)
        else:
            usage()

    except IndexError:
        usage()

if __name__ == '__main__':
    main()
