from __future__ import annotations
import heapq

class Node:
    def __init__(self, value:int|None, probability:int, left:Node|None=None, right:Node|None=None) -> None:
        self.value = value
        self.probability = probability
        self.left = left
        self.right = right
    
    def __lt__(self, other:Node):
        return self.probability < other.probability

def get_probability(data:bytes) -> dict[int, int]:
    probabilities:dict[int, int] = {}
    for value in data:
        if value in probabilities:
            probabilities[value] += 1
        else:
            probabilities[value] = 1

    return probabilities

# Retorna a raíz da árvore de códigos
def get_huffman_codes_tree(probabilities:dict[int, int]) -> Node:
    heap:list[Node] = []

    for value, probability in probabilities.items():
        heapq.heappush(heap, Node(value, probability))

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        combined_probability = node1.probability + node2.probability
    
        heapq.heappush(heap, Node(None, node1.probability + node2.probability, left=node1, right=node2))
    
    return heap[0]

def get_codes(root:Node) -> dict[int, str]:
    codes:dict[int, str] = {}
    __get_codes_r(root, codes)
    return codes

def __get_codes_r(node:Node, codes:dict[int, str], current_code:str='') -> None:
    if node.value is not None:
        codes[node.value] = current_code
    else:
        __get_codes_r(node.left, codes, current_code + '0')
        __get_codes_r(node.right, codes, current_code + '1')

def compress(data:bytes) -> tuple[str, dict[int, str]]:
    probabilities = get_probability(data)
    codes_tree = get_huffman_codes_tree(probabilities)
    codes = get_codes(codes_tree)
    compressed_bits = ''

    for value in data:
        compressed_bits += codes[value]

    return compressed_bits, codes, probabilities

def write_compressed_file(compressed_bits:str, codes:dict[int, str], output_file:str):
    header = bytearray()
    try:
    # TODO CONSERTAR: HEADER NÃO PODE CONVERTER CODIGOS PRA INT, TEM QUE GUARDAR O CÓDIGO INTEIRO
        for value, code in codes.items():
            header.append(value)
            header.append(int(code, 2))
    except ValueError:
        print(value, code)
    header_size = len(header)

    compressed_bytes = bytearray()
    for i in range(0, len(compressed_bits), 8):
        byte = compressed_bits[i : i+8]
        compressed_bytes.append(int(byte, 2))

    with open(output_file, 'wb') as f:
        f.write(header_size.to_bytes(1, 'big'))
        f.write(header)
        f.write(compressed_bytes)

def write_codes(codes:dict[int, str], probabilities:dict[int, int]):
    with open('codes.txt', 'w') as fcodes:
        for value, code in codes.items():
            fcodes.write(f'{chr(value) if 33 <= value <= 126 else value} ({probabilities[value]}) : {code}\n')

def decompress():
        ...






with open('teste.txt', 'rb') as fin:
    data = fin.read()
    compressed_bits, codes, probabilities = compress(data)
    write_codes(codes, probabilities)
    write_compressed_file(compressed_bits, codes, 'out.txt')
