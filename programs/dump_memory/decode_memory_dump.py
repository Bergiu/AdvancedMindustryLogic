import math
from typing import List
from decode_number_to_char_7bit import decode_char


memory_size = 64
display_size = 256
number_size = 7
cell_size = 52
amount_chars_per_cell = math.ceil(cell_size / number_size)  # 8


def decode_memory_dump(inp: str) -> List[int]:
    cell = 0
    cells = []
    i = 0
    for char in inp:
        number = decode_char(char)
        moved_number = number << ((i % amount_chars_per_cell) * number_size)
        cell |= moved_number
        i += 1
        if i % amount_chars_per_cell == 0:
            cells.append(cell)
            cell = 0
    return cells


def decode_memory_dumps(inputs: List[str]) -> List[int]:
    cells = []
    for inp in inputs:
        cells.extend(decode_memory_dump(inp))
    return cells


def test():
    inp1 = "¬xöJaaaa°RöJaaaa77öJaaaaq_öJaaaa(¢öJaaaaÜfüJaaaaiyüJaaaaKQüJaaaaE#üJaaaa5äüJaaaa3gÄJaaaa<yÄJaaaarPÄJaaaar8ÄJaaaaR#ÄJaaaa`äÄJaaaaÜ¢ÄJaaaakgÖJaaaaIyÖJaaaa)QÖJaaaa[7ÖJaaaaħ'ÖJaaaaEäÖJaaaa1¢ÖJaaaa.fÜJaaaa¼xÜJaaaaiQÜJaaaaU7ÜJaaaa?'ÜJaaaa€}ÜJaaaad¢ÜJaaaaIf€Jaaaa"
    inp2 = "3x€Jaaaa>P€Jaaaaþ6€Jaaaa5]€Jaaaa<½€Jaaaa½d»Jaaaajw»Jaaaas6»JaaaaK+»Jaaaa$]»Jaaaaö½»Jaaaaæd«Jaaaaxw«JaaaaWO«Jaaaa·´«Jaaaa?]«JaaaaQ¼«Jaaaaje·JaaaaYw·Jaaaa§O·Jaaaaö5·Jaaaaы*·Jaaaa_{·Jaaaa3½·Jaaaa:d…Jaaaa2u…JaaaaßM…JaaaaV5…Jaaaa`*…Jaaaa·[…Jaaaas½…JaaaaJdøJaaaa"
    cells = decode_memory_dumps([inp1, inp2])
    should = [75009010, 75011546, 75013692, 75016208, 75020741, 75023078, 75025416, 75027748, 75032478, 75034810, 75039544, 75041879, 75043985, 75046545, 75048875, 75051210, 75053542, 75055882, 75058210, 75060550, 75062878, 75065209, 75067550, 75069878, 75072211, 75074544, 75076872, 75079214, 75081544, 75083879, 75086211, 75088546, 75090872, 75093206, 75095549, 75100090, 75102423, 75104753, 75107081, 75111826, 75114148, 75116481, 75118818, 75121141, 75123479, 75125808, 75130346, 75132872, 75135018, 75137545, 75139890, 75142208, 75144546, 75146878, 75149008, 75151544, 75153874, 75156023, 75158345, 75160879, 75163210, 75165546, 75167890, 75170211]
    assert cells == should


if __name__ == '__main__':
    import sys
    inp = open(sys.argv[1]).read().split("\n")
    inputs = []
    cur = None
    for line in inp:
        if cur is None:
            cur = line
        else:
            inputs.append((cur, line))
            cur = None
    decoded_list = []
    for inp1, inp2 in inputs:
        example_data = decode_memory_dumps([inp1, inp2])
        decoded_list.extend(example_data)
    print(decoded_list)
