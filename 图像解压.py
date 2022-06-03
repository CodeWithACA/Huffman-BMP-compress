import time


def bytes_to_binary_string(a: bytes) -> str:
    s = ''
    for item in a:
        s += "{0:b}".format(item).zfill(8)
    return s


def decompress(input_path: str, new_file_name: str):
    decompress_dict = {}
    data_cnt = 0
    data_str = ''
    search_cnt = 1
    cnt = 0
    with open(input_path, 'rb') as input_file:
        head = input_file.read(54)

        # 获取位图数据
        input_file.seek(-4, 2)
        length_of_data_cnt = input_file.read(1)
        length_of_data_cnt = int(length_of_data_cnt.hex(), 16)
        data_cnt = input_file.read()
        data_cnt = bin(int(data_cnt.hex(), 16))[2:2+length_of_data_cnt]
        data_cnt = int(data_cnt, 2)
        input_file.seek(54)  # 指针复原

        with open(new_file_name+'.bmp', 'wb') as output_file:
            output_file.write(head)  # 把文件头原封不动写进去
            length_data = input_file.read(1)  # 获取字典长度
            length = int(length_data.hex(), 16)+1  # 压缩时减去的现在加回来

            # 创建字典
            for _ in range(length):
                l_data = input_file.read(1)
                l = int(l_data.hex(), 16)
                if l % 8 == 0:
                    key_len = l//8
                else:
                    key_len = l//8+1
                key = bytes_to_binary_string(input_file.read(key_len))
                key = key[-l:]    # 切除指定路径
                value_data = input_file.read(1)
                value = hex(int(value_data.hex(), 16))
                value = value[2:]
                decompress_dict[key] = value

            # 还原数据
            while cnt < data_cnt:
                temp = bin(int(input_file.read(1).hex(), 16))[2:]
                l = len(temp)
                for _ in range(8-l):
                    temp = '0'+temp
                data_str = data_str+temp
                while search_cnt < len(data_str)+1:
                    try:
                        l = len(decompress_dict[data_str[:search_cnt]])
                    except KeyError:
                        search_cnt += 1
                        continue
                    else:
                        if l == 1:
                            output_file.write(bytes.fromhex(
                                '0'+decompress_dict[data_str[:search_cnt]]))
                        else:
                            output_file.write(bytes.fromhex(
                                decompress_dict[data_str[:search_cnt]]))
                        data_str = data_str[search_cnt:]
                        search_cnt = 1
                        cnt += 1


if __name__ == '__main__':
    start = time.time()
    decompress('D:\WorkPlace\算法\作业\图像压缩\PeppersRGB.aca', 'output')
    end = time.time()
    print('解压用时{:.3f}秒'.format(end-start))
