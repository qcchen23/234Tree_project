class TreeNode(object):
    # key
    # because the trees are 2-3-4 trees, there could be more than 2 child nodes
    # therefore, children are stored in a list
    def __init__(self, key):
        self.key = key
        self.child = []

def print_tree(root, indent = 0):
    #recursively prints node keys in the tree

    # base case, tree only has root
    if root != None:
        print(indent * " ", root.key)

        # recursive call, executed if child is not null
        if root.child != None:
            for n in range(0, len(root.child)):
                print_tree(root.child[n], indent + 4)

def search(root, elem):
    if root != None:

        if root.key == elem:
            print("Found element", elem, "at position,", root)
            return 1

        else:
            # recursive call, look for element in the child nodes
            if root.child != elem:
                for n in range(0, len(root.child)):
                    search(root.child[n], elem)

def position_checker(number, node):
    # helper function to check for which child to proceed onto
    # could probably be optimized

    if not isinstance(node.key, list):
        if number >= node.key:
            return 1
        else:
            return 0

    elif len(node.key) == 3:
        # three situations:
        # greater than max key
        # smaller than min key
        # in the middle
        if number > max(node.key):
            return 3
        if number < min(node.key):
            return 0
        else:
            if number < node.key[1]:
                return 1
            else:
                return 2
    else:
        if number > max(node.key):
            return 2
        elif number < min(node.key):
            return 0
        else:
            return 1

def bettersearch(root, elem):
    # toward a better search algorithm
    # O(log(n)) runtime

    if root != None:

        # found element which is the only key in the node
        if root.key == elem:
            print(" - Found element", elem)
            return root.key

        # found element which is one of multiple keys in the node
        elif not isinstance(root.key, int) and elem in root.key:
            print(" - Found element", elem, "as one of the keys")
            return root.key

        # element is not in the tree
        elif root.child == []:
            print(" - Input element", elem, "is not found")
            return None

        # recursive case, prints which child the program is checking
        # onward to the next level with the help of position checker
        else:
            index = position_checker(elem, root)
            print(" - Checking child", index, "of current node...")
            return bettersearch(root.child[index], elem)

def split_child(node, x):

    # find which key in the child node to ascend
    # append this key in the child to current node
    mid_index = len(node.child[x].key) // 2
    rise = node.child[x].key[mid_index]
    if not isinstance(node.key, list):
        node.key = [node.key]
    node.key.append(rise)
    node.key.sort()

    # made a new node for the keys after the middle index
    # append this node to child list, then sort child
    new_node = TreeNode(node.child[x].key[(mid_index+1):])
    node.child.append(new_node)
    child_quicksort(node)
    new_node.child = node.child[x].child[(mid_index+1):]

    # update the i-th child to only contain the keys before the middle index
    node.child[x].key = node.child[x].key[:mid_index]
    node.child[x].child = node.child[x].child[:mid_index]

def split_root(root):
    # root node is full
    # Insert new root node

    # save key in root somewhere else to make space for new root
    old_root = root
    root = TreeNode(None)

    # find the middle key to ascend into the new root
    mid_index = len(old_root.key) // 2
    rise = old_root.key[mid_index]
    root.key = rise

    # update the children of new root
    new_node = TreeNode(old_root.key[(mid_index+1):])
    root.child.append(new_node)
    new_node.child = old_root.child[(mid_index+1):]

    old_root.key = old_root.key[:mid_index]
    old_root.child = old_root.child[:mid_index]

    root.child.append(old_root)
    child_quicksort(root)
    return root

def child_quicksort(node):

    i = len(node.child)-1

    while i >= 1:
        if not isinstance(node.child[i].key, list):
            node.child[i].key = [node.child[i].key]
        if not isinstance(node.child[i-1].key, list):
            node.child[i-1].key = [node.child[i-1].key]
        if node.child[i].key[0] < node.child[i-1].key[0]:
            keeper = node.child[i]
            node.child[i] = node.child[i-1]
            node.child[i-1] = keeper
        i -= 1

def insert_nonfull(node,key):
    # inserting into empty node
    if node.key == None:
        node.key = key

    # inserting into non-empty leaf node
    elif node.child == []:
        if isinstance(node.key, list):
            node.key.append(key)
            node.key.sort()

        else:
            node.key = [node.key]
            node.key.append(key)
            node.key.sort()

    # inserting into a non-leaf node
    # goes to the appropriate leaf
    else:
        cpos = position_checker(key,node)
        c = node.child[cpos]

        if isinstance(c.key, list):
            if len(c.key) == 3:
                # c contains 2k-1 keys
                split_child(node, cpos)
                cpos1 = position_checker(key, node)
                c = node.child[cpos1]

        insert_nonfull(c,key)

def insert(root, elem):
    # wrapper function
    # takes care of empty/full node

    # if node as more than one key currently
    if isinstance(root.key,list):

        # root node is full
        # Insert new root node
        if (len(root.key) == 3):
            # save key in root somewhere else to make space for new root
            split_root(root)
            # break point
            insert_nonfull(root, elem)

        # if node  has two keys, not full
        else:
            insert_nonfull(root, elem)

    else:
        insert_nonfull(root, elem)



# main

print("************TEST BEGINS************")
print("Inserting 1, 2, 3, 4, 5, 6 into initially empty tree ..")
root = TreeNode(None)
insert(root,1)
insert(root,2)
insert(root,3)

rt = split_root(root)

insert(rt,4)
insert(rt,5)
insert(rt,6)

print("Printing tree ..")
print_tree(rt)

# bad runtime search, looks for int as well as lists
# uncomment to see it work
#search(root,[5,6,7])

# better runtime search
# only works for int for value comparison reasons
# prints path of searching process to locate the element
print()
print("Searching for key 2 ..")
bettersearch(rt, 2)
print("Searching for key 3 ..")
bettersearch(rt, 3)


# hard-coding the tree, starting from the root
# if there are multiple keys in one node, represented as a list
print()
print("Printing hard-coded tree for further testing ..")
root = TreeNode(8)

test = TreeNode([2,4])
root.child = [test,TreeNode(11)]

root.child[0].child = [TreeNode(1),TreeNode(3),TreeNode([5,6,7])]
root.child[1].child = [TreeNode([9,10]),TreeNode(12)]

print_tree(root)

# search in this tree
print()
print("Searching for key 3 ..")
bettersearch(root, 3)
print("Searching for key 8 ..")
bettersearch(root, 8)
print("Searching for key 10 ..")
bettersearch(root, 10)
print("Searching for key 20 ..")
bettersearch(root, 20)

# split function: split the i-th child given a node
#split_child(test, 2)
#print_tree(root)

# comprehensive insert:
print()

print("Inserting keys 0.2, 18 into the tree ..")
insert(root,0.2)
insert(root,18)

print("Inserting keys 2.2, 2.7 into the tree ..")
insert(root,2.2)
insert(root,2.7)

print("Inserting keys 5.1, 5.8 into the tree ..")
insert(root,5.1)
insert(root,5.8)

print("Inserting keys 10.6, 10.9 into the tree ..")
insert(root,10.6)
insert(root,10.9)


print_tree(root)
