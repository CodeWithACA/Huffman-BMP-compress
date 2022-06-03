import time
# 引入time模块为了计算压缩时间

compress_dict = {}  # 储存 Huffman 树 {'变长码':'对应的原码'}

# 常用函数
# 1 .hex(): bytes->str
# 2 bytes.fromhex(): str->bytes
# 3 int(n,2)： 二进制的n（如1010）转化为十进制，得到的是int
# 4 int(key,2).to_bytes(n,'big')： 把一个int转为2进制，n是字节数


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
    global compress_dict
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
        compress_dict[road] = a.key


def get_keys(d: dict, value: str) -> str:
    for k, v in d.items():
        if value == v:
            return k


def compress(input_path: str):
    global compress_dict
    compress_str = ''   # 储存压缩后的字符串，每次将其前8个写入中间文件
    original_cnt = 0    # 储存源文件大小（字节）
    compress_cnt = 0    # 储存压缩文件大小（字节）
    data_cnt = 0  # 记录纯位图有多少个字节
    with open(input_path, 'rb') as bmpfile:
        head = bmpfile.read(54)
        original_cnt += 54
        with open(input_path[:-4]+'.aca', 'wb') as output:
            output.write(head)
            compress_cnt += 54
            # 把各种颜色出现的次数记录下来
            all_color = {}  # 储存各种颜色对应出现的次数
            while True:
                data = bmpfile.read(1)
                if not data:
                    break
                original_cnt += 1
                if data.hex() in all_color:
                    all_color[data.hex()] += 1
                else:
                    all_color[data.hex()] = 1
            # 构造哈夫曼树
            sorted_all_color = sorted(
                all_color.items(),  key=lambda d: d[1], reverse=True)  # 排序
            huf = HuffmanTree(sorted_all_color)
            get_dict(huf.start)
            # 让指针回到数据开始的地方
            bmpfile.seek(54)

            # 把字典写入中间文件
            length = len(compress_dict)-1   # -1确保能一个字节装下256长的字典
            output.write((length).to_bytes(1, 'big'))    # 第55位表示字典的长度
            for key, item in compress_dict.items():
                l = len(key)
                if l % 8 == 0:
                    key_len = len(key)//8
                else:
                    key_len = l//8+1
                # 用1个字节写key（霍夫曼变长码）会占用几个字节
                output.write(l.to_bytes(1, 'big'))
                compress_cnt += 1
                output.write(int(key, 2).to_bytes(
                    key_len, 'big'))  # 把key转化成二进制
                compress_cnt += key_len
                output.write(bytes.fromhex(item))   # 把value写进去
                compress_cnt += 1

            # 把压缩的数据写入中间文件
            while True:
                original_data = bmpfile.read(1)   # 向下读一位
                if not original_data:
                    l = len((compress_str))
                    if l != 0:
                        for _ in range(8-l):
                            compress_str = compress_str+'0'   # 如果不够8位就在最后补0
                        output.write(int(compress_str, 2).to_bytes(1, 'big'))
                    compress_cnt += 1
                    break
                else:
                    oringinal_data = original_data.hex()  # 把这一位转化成字符串
                    compress_data = get_keys(
                        compress_dict, oringinal_data)    # 在字典中搜索压缩后的字符串
                    compress_str = compress_str+compress_data  # 把这个字符串写入compress_str
                    while len(compress_str) >= 8:
                        output.write(int(compress_str[:8], 2).to_bytes(
                            1, 'big'))  # 把前8位写入中间文件
                        compress_cnt += 1
                        compress_str = compress_str[8:]  # 保留后面的数字

            # 在文件尾巴写上有多少个数据
            data_cnt = original_cnt-54
            # 写入一个数值x，把剩下的读完，成一个字符串s，告诉s的前x位表示的是有多少个数据
            data_cnt = str(data_cnt)
            data_cnt = bin(int(data_cnt, 10))[2:]  # 得到一个二进制字符串
            l_of_data_cnt = len(data_cnt)
            output.write(l_of_data_cnt.to_bytes(1, 'big'))
            while True:
                if len(data_cnt) >= 8:
                    output.write(int(data_cnt[:8], 2).to_bytes(
                        1, 'big'))
                    data_cnt = data_cnt[8:]
                else:
                    for _ in range(8-(len(data_cnt))):
                        data_cnt = data_cnt+'0'   # 如果不够8位就在最后补0
                    output.write(int(data_cnt, 2).to_bytes(1, 'big'))
                    break
    print('压缩率(compression rate)为  {:.3f} %'.format(
        compress_cnt*100/original_cnt))


if __name__ == '__main__':
    start = time.time()
    compress('D:\WorkPlace\算法\作业\图像压缩\PeppersRGB.bmp')
    end = time.time()
    print('压缩用时{:.3f}秒'.format(end-start))
