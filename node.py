__student_name__ = 'Klarissa Jutivannadevi'
__student_id__ = '32266014'


class Node:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.child = [None] * (126 - 36 + 1)
        self.parent = None
        # the index (only contained in the last part)
        self.suffix_index = None
        # suffix link
        self.suffix_link = None


