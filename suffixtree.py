__student_name__ = "Klarissa Jutivannadevi"
__student_id__ = "32266014"

"""
Note:
This code was written per line based on the explanation on GeeksForGeeks. I focused on the steps explained in Part 4 
and Part 5 and modify the code after reading each phase. In the debugging process, I did look at the code from Part 6.
Reference:
https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-4/
https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-5/
https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-6/
J is added later on in order to find suffix array quicker during dfs.
"""


from node import Node

# GLOBAL_END uses a list since it points to an address of the list, hence could change.
GLOBAL_END = [0]
MINIMUM_ASCII = 36


class SuffixTree:
    def __init__(self, word):
        self.word = word
        self.root = Node(-1, [-1])
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.newest_internal_node = None
        self.remaining = 0
        self.last_j = 0
        self.suffix_array = []

    def ukkonen_algorithm(self):
        word = self.word
        for i in range(len(word)):
            # RULE 1: Adds new letter to the existing leaf.
            # Trick: Once a leaf, always a leaf. For all the suffix that has been created, in only needs an extension
            # of letter.
            GLOBAL_END[0] += 1
            # Reset the newest_internal_node at the start of each phase
            self.newest_internal_node = None
            self.remaining += 1

            # The number of suffixes left that is not created in the tree.
            while self.remaining > 0:
                # if no active length, edge will be the most recent letter (in this case stored by index)
                if self.active_length == 0:
                    self.active_edge = i

                # Rule 2B: add branch from active node (no new split node required)
                if self.active_node.child[ord(word[self.active_edge]) - MINIMUM_ASCII] is None:
                    new_node = Node(i, GLOBAL_END)
                    # the new node that is created represent the suffix is recently put. Since the suffix should be
                    # created in order, last_j starts from index 0
                    new_node.suffix_index = self.last_j
                    # update the new_node parent to current_node
                    new_node.parent = self.active_node
                    # change the child to that instead of None
                    self.active_node.child[ord(word[self.active_edge]) - MINIMUM_ASCII] = new_node

                    # Update the suffix link based on the active node
                    if self.newest_internal_node is not None:
                        self.newest_internal_node.suffix_link = self.active_node
                        self.newest_internal_node = None

                # if not None, go to the child.
                else:
                    created_child_node = self.active_node.child[ord(word[self.active_edge]) - MINIMUM_ASCII]
                    # Trick: skip/count trick where the skip happens if the active_length is greater or equal to the
                    # length of the current internal node. The child node will then be the active node since it goes
                    # down and so the active_length can be subtracted indicating the active_length that is left to be
                    # computed and active_edge increase to indicate how much it moves forward
                    if self.active_length >= created_child_node.end[0] - created_child_node.start + 1:
                        self.active_node = created_child_node
                        self.active_edge += created_child_node.end[0] - created_child_node.start + 1
                        self.active_length -= created_child_node.end[0] - created_child_node.start + 1
                        # if successful, move to the next iteration
                        continue

                    # RULE 3: Do nothing (when no changes happen to the tree)
                    # Trick: showstopper. if rule 3 is detected, go to next phase immediately
                    if word[i] == word[created_child_node.start + self.active_length]:
                        if self.newest_internal_node is not None and self.active_node is not self.root:
                            # update the suffix link of the node
                            self.newest_internal_node.suffix_link = self.active_node
                            self.newest_internal_node = None
                        # active_length added since a new letter (current letter) is not yet put anywhere
                        self.active_length += 1
                        # go to next phase
                        break

                    # Rule 2A: A new internal node and a new leaf is created
                    split_end = created_child_node.start + self.active_length - 1
                    # create a new internal node (split node)
                    mid_split = Node(created_child_node.start, [split_end])
                    # assign the parent, which is the parent of the previous node that is going down.
                    mid_split.parent = created_child_node.parent
                    mid_split.suffix_link = self.root

                    # put the current node as children of the new internal node
                    mid_split.child[ord(word[split_end + 1]) - MINIMUM_ASCII] = created_child_node
                    # update the parent child to mid_split replacing current_node
                    created_child_node.parent.child[ord(word[created_child_node.start]) - MINIMUM_ASCII] = mid_split

                    # update the status of current_node (start position moved down and parent changed to internal node)
                    created_child_node.start = split_end + 1
                    created_child_node.parent = mid_split

                    # create a new node for the new branch
                    mid_new_child = ord(word[i]) - MINIMUM_ASCII
                    new_child = Node(i, GLOBAL_END)
                    new_child.suffix_index = self.last_j
                    mid_split.child[mid_new_child] = new_child
                    new_child.parent = mid_split

                    # change the suffix link if there is an internal node that has been created before
                    if self.newest_internal_node is not None:
                        self.newest_internal_node.suffix_link = mid_split

                    # update the recent internal node to the most recent one
                    self.newest_internal_node = mid_split

                self.last_j += 1
                self.remaining -= 1

                # extend the active length to the next edge (basically keep on running rule 2)'
                if self.active_node is not self.root:
                    # Follow the suffix link
                    self.active_node = self.active_node.suffix_link
                # update the active_edge to the next index
                elif self.active_length > 0 and self.active_node is self.root:
                    self.active_edge = i - self.remaining + 1
                    self.active_length -= 1

    def dfs(self, node):
        visited = []
        self.dfs_traversal(node, visited)

    def dfs_traversal(self, current_node, visited):
        visited.append(current_node)
        for child_node in current_node.child:
            if child_node is not None and child_node not in visited:
                if child_node.suffix_index is not None:
                    self.suffix_array.append(child_node.suffix_index)
                self.dfs_traversal(child_node, visited)



