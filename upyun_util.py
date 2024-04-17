import upyun
from urllib.parse import quote
import os


up = upyun.UpYun('magiclizi', username='lizi', password='ll09280416')


def get_face_list(dir_name):
    list = []
    res = up.getlist(dir_name)
    for i in range(len(res)):
        f = res[i]
        name = f['name']
        t = f['type']
        if t == 'F':
            sub_dir_name = dir_name + '/' + name
            list.extend(get_face_list(sub_dir_name))
        else:
            list.append({
                'name': name,
                'url': f'https://files.magiclizi.com/{dir_name}/{quote(name)}'
            })
    return list


def upload(file):
    path_parts = file.split(os.sep)[-2:]
    file_name = f"{path_parts[0]}-{path_parts[1]}"
    # print(path_parts)
    upyunurl = f"/fakeface/upload/{file_name}"
    with open(file, 'rb') as f:
        res = up.put(upyunurl, f)
        # print(res)
        return "https://files.magiclizi.com" + upyunurl



