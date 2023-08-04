__student_name__ = 'Klarissa Jutivannadevi'
__student_id__ = '32266014'

import sys
from suffixtree import SuffixTree


def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()
    return line


input_word = read_file(sys.argv[1])[0] + '$'


def process(word):
    st = SuffixTree(word)
    st.ukkonen_algorithm()
    st.dfs(st.root)
    for i in range(len(st.suffix_array)):
        st.suffix_array[i] = str(st.suffix_array[i] + 1)
    return st.suffix_array


if __name__ == '__main__':
    output = process(input_word)
    with open('output_sa.txt', 'w') as f:
        f.write('\n'.join(output))
