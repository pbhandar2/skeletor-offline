class SplayTree:
    def __init__(self):
        self.root = None
        self.num_nodes = 0
        self.keys = []

    def find(self, key):

        cur_node = self.root
        prev_node = None
        reuse_distance = 0

        while cur_node is not None:
            prev_node = cur_node
            if cur_node.key > key:
                cur_node = cur_node.left
                reuse_distance += 1
            elif cur_node.key < key:
                cur_node = cur_node.right
                reuse_distance += 1
            else:
                self.splay(cur_node)
                return reuse_distance
        else:
            new_node = Node(key)
            self.insert(prev_node, new_node)
            self.keys.append(key)
            self.splay(new_node)
            return -1

    def insert(self, parent, child):

        if self.root is None:
            self.root = child
        else:
            if parent.key > child.key:
                parent.left = child
            else:
                parent.right = child
            child.parent = parent

    def splay(self, node):

        while self.root != node:

            if node.parent == self.root:
                self.zig(node)
            else:
                parent_node = node.parent
                grand_parent_node = parent_node.parent

                if node == parent_node.left and parent_node == grand_parent_node.left:
                    self.zig_zig(node, "right")
                elif node == parent_node.right and parent_node == grand_parent_node.right:
                    self.zig_zig(node, "left")
                elif node == parent_node.left and parent_node == grand_parent_node.right:
                    self.zig_zag(node, "right")
                else:
                    self.zig_zag(node, "left")

    def zig(self, node):

        if node.key > self.root.key:
            self.rotate_left(node)
        else:
            self.rotate_right(node)

        self.swap_parents(node)
        self.root = node

    def zig_zig(self, node, side):

        if side == "right":

            self.rotate_right(node.parent)
            self.swap_parents(node.parent)

            if node.parent == self.root:
                self.zig(node)
            else:
                self.rotate_right(node)
                self.swap_parents(node)

        else:
            self.rotate_left(node.parent)
            self.swap_parents(node.parent)

            if node.parent == self.root:
                self.zig(node)
            else:
                self.rotate_left(node)
                self.swap_parents(node)

    def zig_zag(self, node, side):

        if side == "right":
            self.rotate_right(node)
            self.swap_parents(node)

            if node.parent == self.root:
                self.zig(node)
            else:
                self.rotate_left(node)
                self.swap_parents(node)
        else:
            self.rotate_left(node)
            self.swap_parents(node)

            if node.parent == self.root:
                self.zig(node)
            else:
                self.rotate_right(node)
                self.swap_parents(node)

    @staticmethod
    def rotate_right(node):

        node.parent.left = node.right

        if node.right is not None:
            node.right.parent = node.parent

        node.right = node.parent

    @staticmethod
    def rotate_left(node):

        node.parent.right = node.left

        if node.left is not None:
            node.left.parent = node.parent

        node.left = node.parent

    def swap_parents(self, node):
        parent_node = node.parent
        grand_parent_node = parent_node.parent

        node.parent = grand_parent_node
        parent_node.parent = node

        if parent_node == self.root:
            self.root = node
        else:
            if grand_parent_node.key > parent_node.key:
                grand_parent_node.left = node
            else:
                grand_parent_node.right = node

    def reverse_in_order(self, node, indent):
        if node is not None:
            indent += 5
            self.reverse_in_order(node.right, indent)

            for i in range(indent):
                print(" ", end="")

            print(node.key)

            self.reverse_in_order(node.left, indent)


class Node:
    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None
        self.parent = None