from parser import *

def create_tree(formula, predicates):
    "Creates tree from formula"

    form = formula[1:-1]
        
    new = list()
    string=""
    wait1 = False
    wait2=False
    wait3=False
    left=0
    right=0
    
    for f in form:
        if f in ["zeroin", "sing", "exists", "forall"]:
            string = f
            wait1 = True
        elif f in ["sub", "succ", "<"]:
            string = f
            wait1=True
            wait2=True
        elif wait1:
            if f=='(':
                wait3=True
                continue
            string+=" "
            string+=f
            wait1 = False
            if not wait2:
                new.append(string)
                string=""
        elif wait2:
            string+=" "
            string+=f
            wait2=False
            new.append(string)
            string=""
        elif wait3:
            if f==')':
                wait3=False
                continue
        else:
            new.append(f)

    root = tree_from_formula(new, 0, len(new)-1, predicates)
    order = level_order(root)
    write(order, "tree.gv")
    
    root = change_tree(root)
    order = level_order(root)
    write(order, "tree.gv")
    
    a = create_aut(root)
    write_to_gv(a, "graph.gv")
    write_to_file(a, "a.ba")

class newNode:
    "New tree node"

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def level_order(root):
    "Creates level order of a tree"

    if root == None: # empty tree
        return
        
    # level order
    queue = [root]
    order = list()
    while(len(queue)>0):
        order.append(queue[0].data)
        node = queue.pop(0)
        if node.left != None:
            queue.append(node.left)
        if node.right != None:
            queue.append(node.right)
            
    # insert None
    i=0
    while i < len(order):
        # the rest is None
        if all(order[j]==None for j in range(i, len(order))):
            break
        # None nodes have None children
        if order[i] == None:
            order.insert(2*i+1, None)
            order.insert(2*i+2, None)
        # parent is None
        elif i>0 and order[(i-1)%2]==None:
            order.insert(i, None)
        # neg, exists and forall nodes has only one child
        elif order[i] == "neg" or order[i].find("exists")!=-1 or order[i].find("forall")!=-1:
            order.insert(2*i+2, None)
        # zeroin, sub, succ and sing nodes has no children
        elif order[i].find("zeroin")!=-1 or order[i].find("succ")!=-1 or order[i].find("sing")!=-1 or order[i].find("sub")!=-1 or len(order[i])==1 or order[i].find("<")!=-1:
            order.insert(2*i+1, None)
            order.insert(2*i+2, None)
        i+=1

    return order

def write(order, f):
    "Writes tree in f (.gv file)"

    with open(f, "w") as f:
        f.write("digraph Tree {\n")
        f.write('\tnode[footname="Arial"];\n')
       
        j=0
        new = list()
        for o in order:
            if o != None:
                f.write('\t{} [label="{}"]'.format(j, o))
            new.append(j)
            j+=1

        for i in range(len(new)):
            if order[i]==None:
                continue
            if ((2*i+1) < len(new)) and order[2*i+1]!=None:
                f.write('\t"{}" -> "{}";\n'.format(new[i], new[2*i+1]))
            if ((2*i+2) < len(new)) and order[2*i+2]!=None:
                f.write('\t"{}" -> "{}";\n'.format(new[i], new[2*i+2]))
        f.write("}\n")

def get_index(formula, start, end):
    if (start > end): # wrong indices
        return -1

    stack=[]
    for i in range(start, end+1): # from start to end
        if formula[i]=='(':
            stack.append(formula[i])
        elif (formula[i]==')'):
            if (stack[-1] == '('):
                stack.pop(-1)
                if len(stack)==0:
                    return i # index of last ')'
    return -1

def tree_from_formula(formula, start, end, predicates):
    "Creates tree from formula"

    if (start > end): # end of recursion
        return None
        
    if formula[start] in predicates.keys():
        # do not divide atomic automata and predicates from arguments
        new=list()
        string=""
        skip=False
        skip2=False
        right=[]
        nop=False
        for word in predicates[formula[start]][1][1:-1].split():
            while word[0]=="(":
                new.append("(")
                word=word[1:]
            while word[-1]==")":
                word=word[:-1]
                right.append(")")
            if word in ["zeroin", "sing", "exists", "forall"]:
                skip=True
                string=word
            elif word in ["sub", "succ", "<"]:
                skip=True
                skip2=True
                string=word
            else:
                if skip:
                    string+=" "
                    if word in predicates[formula[start]][0]:
                        index = predicates[formula[start]][0].index(word)
                        string+=formula[start+index+1]
                    else:
                        string+=word
                    skip=False
                    if not skip2:
                        new.append(string)
                        while len(right)>0:
                            new.append(right.pop())
                elif skip2:
                    skip2=False
                    string+=" "
                    if word in predicates[formula[start]][0]:
                        index = predicates[formula[start]][0].index(word)
                        string+=formula[start+index+1]
                    else:
                        string+=word
                    new.append(string)
                    while len(right)>0:
                        new.append(right.pop())
                else:
                    new.append(word)
                    while len(right)>0:
                        new.append(right.pop())
        while new[0][0]=="(":
            new = new[1:]
        while new[0][-1]==")":
            new = new[:-1]
        print(new)
        root = tree_from_formula(new, 0, len(new)-1, predicates)
    else:
        root = newNode(formula[start]) # new node
    index = -1

    if (start+1 <= end and formula[start+1] == '('):
        index = get_index(formula, start+1, end) # index of last ')'
    if index != -1:
        root.left = tree_from_formula(formula, start+2, index-1, predicates)
        root.right = tree_from_formula(formula, index+2, end-1, predicates)

    return root

def change_tree(root):
    
    # all nodes
    queue=[root]
    while len(queue) > 0:
        node=queue.pop(0)
        if node.left != None and node.left.left != None:
            # forall
            if node.data.find("forall")!=-1 and node.left.data == "neg":
                node.left.data = node.data.replace("forall", "exists")
                node.data = "neg"
            if node.data == "neg" and node.left.data.find("forall")!=-1:
                node.data = node.left.data.replace("forall", "exists")
                node.left.data = "neg"
            if node.data.find("forall")!=-1 and node.left.data == "implies":
                node.left.data = node.data.replace("forall", "exists")
                node.data = "neg"
                tmp_left = node.left.left
                tmp_right = node.left.right
                node.left.right = None
                node.left.left = newNode("and")
                node.left.left.left = tmp_left
                node.left.left.right = newNode("neg")
                node.left.left.right.left = tmp_right
                node.left.left.right.right = None
            # implication
            if node.data == "implies" and node.left.data == "neg":
                node.data = "or"
                node.left = node.left.left
            if node.data == "implies" and node.left.data.find("forall")!=-1:
                node.data = "or"
                node.left.data = node.left.data.replace("forall", "exists")
                tmp = node.left.left
                node.left.left = newNode("neg")
                node.left.left.left = tmp
            # two neg in a row
            if root.data == "neg" and root.left.data == "neg":
                root = root.left.left
            if node.left != None and node.left.left != None:
                if node.left.data == "neg" and node.left.left.data=="neg":
                    node.left = node.left.left.left
        if node.right != None and node.right.left != None:
            # two neg in a row
            if node.right.data == "neg" and node.right.left.data=="neg":
                node.right = node.right.left.left
        if node.left != None:
            queue.append(node.left)
        if node.right != None:
            queue.append(node.right)
            
    return root


def create_aut(node):
    if node.data.find("exists")!=-1:
        a=exists(node.data[-1], create_aut(node.left))
    elif node.data.find("forall")!=-1:
        a=comp2(exists(node.data[-1], comp2(create_aut(node.left))))
        print("forall")
    elif node.data == "neg":
        a=comp2(create_aut(node.left))
        print("neg")
    elif node.data == "and":
        a=intersection(create_aut(node.left), create_aut(node.right))
        print("and")
    elif node.data == "or":
        a=union(create_aut(node.left), create_aut(node.right))
        print("or")
    elif node.data == "implies":
        a=union(comp2(create_aut(node.left)), create_aut(node.right))
    elif node.data.find("sub")!=-1:
        a=sub(node.data.split(" ")[1], node.data.split(" ")[2])
    elif node.data.find("succ")!=-1:
        a=succ(node.data.split(" ")[1], node.data.split(" ")[2])
    elif node.data.find("zeroin")!=-1:
        a=zeroin(node.data.split(" ")[1])
    elif node.data.find("sing")!=-1:
        a=sing(node.data.split(" ")[1])
    elif node.data.find("<")!=-1:
        a=less(node.data.split(" ")[1], node.data.split(" ")[2])
    return a

