import pdb

class SplayTree():

    def __init__(self):
        self.root = None
        self.keys = []

    def rotate(self, parent, child):

        # check if the child is the left child of parent 
        left_child_flag = 1 if parent.left == child else 0

        # change the connection from the grand parent node 
        grand_parent_node = parent.parent 

        if grand_parent_node != None:
            if grand_parent_node.right == parent:
                grand_parent_node.right = child
            else:
                grand_parent_node.left = child

            # set child parent to be grand parent and 
            child.parent = grand_parent_node
        else:
            child.parent = None
            self.root = child

        # set parent's parent to be the child
        parent.parent = child 

        if left_child_flag:

            # get the right child of child 
            child_right_node = child.right 

            # set the right of the child to the parent 
            child.right = parent
            
            # set the left of the parent to be the right of the child node
            parent.left = child_right_node


        else:

            # get the left child of child
            child_left_node = child.left 

            # set the left of the child to the parent 
            child.left = parent

            # set the right of the parent to be the right of the child node
            parent.right = child_left_node


    def zig_zig(self, node):

        parent_node = node.parent
        grand_parent_node = parent_node.parent

        # if node.key == 4593220:
        #     pdb.set_trace()


        # rotate the grand parent and the parent first 
        self.rotate(grand_parent_node, parent_node)

        # if node.key == 4593220:
        #     pdb.set_trace()

        if not self.parent_is_root(node):
            # rotate the node and the parent 
            self.rotate(parent_node, node)

    def zig_zag(self, node):

        parent_node = node.parent
        grand_parent_node = parent_node.parent

        # if node.key == 786827:
        #     print("LETS SEEEEEEEEEEEEEE")
        #     pdb.set_trace()

        # rotate the node and the parent first
        self.rotate(parent_node, node)

        # if node.key == 786827:
        #     pdb.set_trace()

        if not self.parent_is_root(node):
            # roate the node and the grandparent 
            self.rotate(grand_parent_node, node)



    def find(self, key):

        # if the tree is empty 
        if self.root == None:
            self.insert(key)
            return -1

        # if the key matches the root 
        if self.root.key == key:
            return 0

        #print(self.root.right)
        #print(self.root.left)

        # check where to start looking from 
        cur_node = self.root.left if key < self.root.key else self.root.right
        reuse_distance = 1

        print("CUR NODE is {}".format(cur_node))

        while cur_node != None:

            print("comparing {} and {}".format(key, cur_node.key))

            if key == cur_node.key:
                break

            reuse_distance += 1
            cur_node = cur_node.right if key > cur_node.key else cur_node.left
        else:
            print("KEY NOT FOUND! {}".format(key))
            #pdb.set_trace()
            
            self.insert(key)
            #pdb.set_trace()
            return -1 

        print("KEY FOUND! {}, {}".format(cur_node.key, key))
        #pdb.set_trace()
        self.splay(cur_node)
        return reuse_distance
        
        

    def insert(self, key):

        node = Node(key)
        self.keys.append(key)

        if key == 791706:
            print("CHECKKKKKKKKKKKKKKKKKKKKKKKKKkk")
            pdb.set_trace()

        if self.root == None:
            self.root = node
        else:

            cur_node = self.root

            while cur_node.right != None or cur_node.left != None:
                if cur_node.right == None:
                    print("RIGHT")
                    if key > cur_node.key:
                        cur_node.right = node
                        node.parent = cur_node
                        break
                    else:
                        cur_node = cur_node.left
                elif cur_node.left == None:
                    if key == 791706:
                        print("LEFT")
                        pdb.set_trace()
                    if key < cur_node.key:
                        cur_node.left = node
                        node.parent = cur_node
                        break
                    else:
                        cur_node = cur_node.right
                else:
                    cur_node = cur_node.right if key > cur_node.key else cur_node.left
            else:

                print("IN ELSEEEE")

                if key > cur_node.key:
                    cur_node.right = node
                else:
                    cur_node.left = node

            
                node.parent = cur_node

            print("BROKEN")

            if key == 791706:
                print("CHECKKKKKKKKKKKKKKKKKKKKKKKKKkk")
                pdb.set_trace()

            self.splay(node)

    def zig_left(self, node):

        parent_node = node.parent 
        grand_parent_node = parent_node.parent 

        # replace the left child of parent node with its parent 
        parent_left_node = parent_node.left
        parent_node.left = grand_parent_node

        # replace the right of the grand parent node with the parent
        grand_parent_node.right = parent_right_node

        # change the parent of the grandparent 
        grand_parent_node.parent = parent_node

        if grand_parent_node == self.root:
            parent_node.parent = None 
            self.root = parent_node
        else:

            # change the parent of grandparent to parent
            great_grand_parent_node = grand_parent_node.parent 
            parent_node.parent = great_grand_parent_node

            if great_grand_parent_node.right == grand_parent_node:
                great_grand_parent_node.right = parent_node
            else:
                great_grand_parent_node.left = parent.node

    def zig_right(self, node):

        parent_node = node.parent 
        grand_parent_node = parent_node.parent 

        # replace the right child of parent node with its parent 
        parent_right_node = parent_node.right
        parent_node.right = grand_parent_node

        # replace the left of the grand parent node with the parent
        grand_parent_node.left = parent_right_node

        # change the parent of the grandparent 
        grand_parent_node.parent = parent_node


        if grand_parent_node == self.root:
            parent_node.parent = None 
            self.root = parent_node
        else:

            # change the parent of grandparent to parent
            great_grand_parent_node = grand_parent_node.parent 
            parent_node.parent = great_grand_parent_node

            if great_grand_parent_node.right == grand_parent_node:
                great_grand_parent_node.right = parent_node
            else:
                great_grand_parent_node.left = parent.node



        

    def zig(self, node):

        parent_node = node.parent

        if parent_node == self.root:

            node.parent = None
            parent_node.parent = node 

            if parent_node.right == node:

                left_node = node.left 
                parent_node.right = left_node
                node.left = parent_node

            elif parent_node.left == node:

                right_node = node.right
                parent_node.left = right_node
                node.right = parent_node

            self.root = node

        else:

            if parent_node.right == node:
                print("RIGHT CHILD")
                self.zig_left(node)
            elif parent_node.left == node:
                print("LEFT CHILD")
                self.zig_right(node)
            else: 
                pdb.set_trace()
                print("OHHH HOOOO")

        #pdb.set_trace()


        # root_flag = 0

        # # print("In zig root is {} and parent is {}".format(self.root.key, parent_node.key))

        # # Checking if the grandparent exist or parent is the root
        # if parent_node.parent:

        #     grand_parent_node = parent_node.parent 

        #     # first upgrade child of grandparent node to be current node 
        #     if grand_parent_node.right == parent_node:
        #         grand_parent_node.right = node
        #     else:
        #         grand_parent_node.left = node 

        #     node.parent = grand_parent_node

        # else:
        #     # print("root time")
        #     root_flag = 1

        # print(self.root.key)
        # print(self.root.right)
        # print(self.root.left)
        # print(node.key)

        # check if the node is the left or right child and zip accordingly 


        # if root_flag == 1:
        #     self.root = node
        #     node.parent = None

        # parent_node.parent = node

    def parent_is_root(self, node):

        parent_node = node.parent

        # check if parent is root
        if self.root == parent_node:



            node.parent = None
            parent_node.parent = node 

            if parent_node.right == node:

                left_node = node.left 
                parent_node.right = left_node
                if left_node: 
                    parent_node.right.parent = parent_node
                node.left = parent_node

            elif parent_node.left == node:

                right_node = node.right
                parent_node.left = right_node
                if right_node: 
                    parent_node.left.parent = parent_node
                node.right = parent_node

            self.root = node


            return True

        return False


    def splay(self, node):

        while self.root.key != node.key:

            if not self.parent_is_root(node):
                parent_node = node.parent
                grand_parent_node = parent_node.parent 
                if (parent_node.left == node and
                    grand_parent_node.left == parent_node):
                    print("It is a right right situation")

                    #pdb.set_trace()
                    if not self.parent_is_root(node):
                        self.zig_zig(node)
                    #pdb.set_trace()

                    # if not self.parent_is_root(node):
                    #     self.zig_right(node)

                    # if not self.parent_is_root(node):
                    #     self.zig_right(node)
                elif (parent_node.right == node and
                    grand_parent_node.right == parent_node):
                    print("This is a left left situation")
                    if not self.parent_is_root(node):
                        self.zig_zig(node)
                elif (parent_node.right == node and
                    grand_parent_node.left == parent_node):

                    print("This is a left right situation")

                    if not self.parent_is_root(node):
                        self.zig_zag(node)
                elif (parent_node.left == node and
                    grand_parent_node.right == parent_node):

                    print("This is a right left situation")
                    #pdb.set_trace()
                    # if not self.parent_is_root(node):
                    #     self.zig_right(node)
                    # pdb.set_trace()

                    if not self.parent_is_root(node):
                        self.zig_zag(node)

                    #pdb.set_trace()
                else:
                    print("SO THIS IS THE PROBLEM")
                    print(grand_parent_node.key)
                    print(parent_node.key)
                    print(node.key)

                    pdb.set_trace()

                    print("Parent key is {} and right node is {} and left node is {}"
                        .format(parent_node.key, parent_node.right.key, parent_node.left.key))



            else:
                print("Parent is root")

            #pdb.set_trace()

            #pdb.set_trace()


            



            # grand_parent_node = parent_node.parent 


            # if (parent_node.right == node and
            #     grand_parent_node.right == parent_node):
            #     print("This is a left left situation")
            #     pass
            # elif (parent_node.left == node and
            #     grand_parent_node.left == parent_node):

            #     print("This is a right right situation")
                
                
            #     self.zig_right(node)
            #     pdb.set_trace()

            #     new_parent_node = node.parent

            #     if new_parent_node == self.root:

            #         node.parent = None
            #         new_parent_node.parent = node 

            #         if new_parent_node.right == node:

            #             left_node = node.left 
            #             new_parent_node.right = left_node
            #             node.left = new_parent_node

            #         elif new_parent_node.left == node:

            #             right_node = node.right
            #             new_parent_node.left = right_node
            #             node.right = new_parent_node

            #         self.root = node

            #     else:
            #         self.zig_right(node)


            #     pdb.set_trace()


            #     pass
            # elif (parent_node.left == node and
            #     grand_parent_node.right == parent_node):
            #     print("This is a right left situation")
            #     pass
            # else:
            #     print("This is a left right situation")
            #     pass

            #self.zig(node)
            #print("IN LOOP {} - {}".format(self.root.key, node.key))

        #print("SPLAYING DONE")










class Node():

    def __init__(self, key):
        self.right = None
        self.left = None
        self.key = key
        self.parent = None