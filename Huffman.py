d = {}


class Node(object):
    def __init__(self, key, node_weight):
        self.trace = []
        self.left = None
        self.right = None
        self.node_weight = node_weight
        self.key = key


class HuffmanTree(object):
    def __init__(self, sorted_dict):
        self.tree = sorted_dict
        self.node = []
        for item in self.tree:
            self.node.append(Node(item[0], item[1]))
        while True:
            a = Node('', self.node[-1].node_weight+self.node[-2].node_weight)
            a.left = self.node[-2]
            a.right = self.node[-1]
            self.node = self.node[:-2]
            if self.node == []:
                self.start = a
                break
            # 插入新的
            l = len(self.node)
            for i in range(l):
                if self.node[i].node_weight < a.node_weight:
                    self.node.insert(i, a)
                    break
                elif i == l-1:
                    self.node.append(a)


def get_dict(a: Node) -> dict:
    global d
    if a.left != None:
        a.left.trace.extend(a.trace)
        a.left.trace.append('0')
        get_dict(a.left)
    if a.right != None:
        a.right.trace.extend(a.trace)
        a.right.trace.append('1')
        get_dict(a.right)
    if a.left == None or a.right == None:
        road = ''.join(a.trace)
        d[road] = a.key


if __name__ == '__main__':
    # example = {'a': 5, 'b': 6, 'c': 5, 'd': 7, 'e': 8,
    #            'f': 9, 'g': 2, 'h': 3, 'i': 4, 'j': 5, 'k': 10}
    # example = {'a': 5, 'b': 6, 'c': 5, 'd': 7, 'e': 7,
    #            'f': 9, 'g': 2, 'h': 3, 'i': 4, 'j': 7, 'k': 7}
    # example = {'2': 2, '3': 3, '4': 4}
    example = {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 1,
               'f': 1, 'g': 1, 'h': 1, 'i': 1, 'j': 3, 'k': 2}

    sorted_example = sorted(example.items(),  key=lambda d: d[1], reverse=True)
    print(sorted_example)
    huf = HuffmanTree(sorted_example)
    get_dict(huf.start)
    print(d)
