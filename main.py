import upyun_util
import fooocus
from typing import Annotated
from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import json
from urllib.parse import urlparse
import os
import threading
import time
import random
import string
import jwt
import math
import azure

JWT_SECRET = "dfasklfjsafusaiuqwnwenwq,melikjdlksa"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
length = 10
face_config = {}
default_face =  "https://files.magiclizi.com/default.png"
with open("./ff.json", 'r', encoding='utf-8') as file:
    # 解析文件内容到Python数据结构
    data = json.load(file)
    for item in data:
        face_config[item['name']] = item

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应更精确地设置
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)
import logging
logging.getLogger('uvicorn').setLevel(logging.CRITICAL)
logging.getLogger('uvicorn.access').setLevel(logging.CRITICAL)


def decode_jwt(token: str):
    try:
        decoded_jwt = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return decoded_jwt
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


@app.post('/login')
async def login(mobile: Annotated[str, Form()]):
    with open("./user.json", 'r', encoding='utf-8') as file:
        # 解析文件内容到Python数据结构
        data = json.load(file)
        if mobile in data:
            jwt_token = jwt.encode({"user": mobile, "time_stamp": int(time.time())}, JWT_SECRET, algorithm="HS256")
            return {"code": 200, "token": jwt_token}
        else:
            return {"code": 500}


@app.get('/')
async def root():
    # rst_list = upyun_util.get_face_list("/fakeface/face")
    # print(len(rst_list))
    rst = azure.translate("你好,我好")
    return {"message": rst}


@app.get('/check_in_use')
async def in_use():
    return {"code": 200, "data": {
        "in_use": fooocus.in_use
    }}


@app.get("/library")
async def get_face_library(page: int = 1, token: str = Depends(oauth2_scheme)):
    if page < 1:
        return {"code": 500, "msg": "page Error Must >= 1"}
    else:
        rst_list = upyun_util.get_face_list("/fakeface/face")
        page_cnt = 30
        total_page = math.ceil(len(rst_list) / page_cnt)
        start = (page - 1) * page_cnt
        end = start + page_cnt
        sub_list = rst_list[start:end]
        # print(sub_list)
        return {"code": 200, "data": {"list": sub_list, "total_page": total_page}}


@app.get("/key")
async def get_key_cache(key: str = 1):
    if key in fooocus.deal_cache:
        rst = fooocus.deal_cache[key]
        # print(rst)
        return {"code": 200, "data": rst}
    else:
        return {"code": 500, "data": {}}


@app.get("/keys")
async def get_keys(keys: str, token: str = Depends(oauth2_scheme)):
    key_list = json.loads(keys)
    ret_list = []
    for key in key_list:
        if key in fooocus.deal_cache:
            rst = fooocus.deal_cache[key]
            ret_list.append({
                "key": key,
                "rst": rst
            })
        else:
            print(f"key {key} not exist")
    # print(ret_list)
    return {"code": 200, "data": {"list": ret_list}}


@app.get("/bg_prompts_conf")
async def get_bg_conf(token: str = Depends(oauth2_scheme)):
    user = decode_jwt(token)
    with open("./bg_prompts.json", 'r', encoding='utf-8') as file:
        # 解析文件内容到Python数据结构
        data = json.load(file)
        return {"code": 200, "data": data}


@app.post("/swap_bg_batch")
async def swap_bg_batch(targets: Annotated[str, Form()], select_p: Annotated[str, Form()], custom_p: Annotated[str, Form()], token: str = Depends(oauth2_scheme)):
    print("swap_bg_batch")
    print(targets)
    print(select_p)
    print(custom_p)
    if custom_p != "none":
        rst = azure.translate(custom_p)
        print(f"需要翻译 {custom_p} to {rst}")
        select_p = f"{select_p},{rst}"
    user = decode_jwt(token)
    user_key = user["user"]
    with open("./user.json", 'r', encoding='utf-8') as file:
        # 解析文件内容到Python数据结构
        data = json.load(file)
        if user_key in data:
            rst = data[user_key]
            client = rst['client']
            targets_list = json.loads(targets)
            keys = []
            cnt = 6
            for target in targets_list:
                timestamp_ms = int(time.time() * 1000)
                chars = string.ascii_letters
                random_string = ''.join(random.choice(chars) for _ in range(length))
                key = f'{timestamp_ms}{random_string}'
                target["key"] = key
                fooocus.deal_cache[key] = {"finish": False, "progress": 0, "cnt": f"0/{cnt}"}
                keys.append(key)
            thread = threading.Thread(target=batch, args=(targets_list, default_face, cnt, 0, select_p, False, client))
            thread.start()
            return {"code": 200, "data": {"keys": keys}}
        else:
            return {"code": 500, "data": {}}


@app.post("/swap_face_batch")
async def swap_face_batch(face_url: Annotated[str, Form()], targets: Annotated[str, Form()], token: str = Depends(oauth2_scheme)):
    print("swap_face_batch")
    user = decode_jwt(token)
    user_key = user["user"]
    with open("./user.json", 'r', encoding='utf-8') as file:
        # 解析文件内容到Python数据结构
        data = json.load(file)
        if user_key in data:
            rst = data[user_key]
            client = rst['client']
            targets_list = json.loads(targets)
            keys = []
            cnt = 4
            for target in targets_list:
                timestamp_ms = int(time.time() * 1000)
                chars = string.ascii_letters
                random_string = ''.join(random.choice(chars) for _ in range(length))
                key = f'{timestamp_ms}{random_string}'
                target["key"] = key
                fooocus.deal_cache[key] = {"finish": False, "progress": 0, "cnt": f"0/{cnt}"}
                keys.append(key)
            thread = threading.Thread(target=batch, args=(targets_list, face_url, cnt, 0, None, True, client))
            thread.start()
            return {"code": 200, "data": {"keys": keys}}
        else:
            return {"code": 500, "data": {}}


@app.post("/detail_batch")
async def detail_batch(face_url: Annotated[str, Form()], targets: Annotated[str, Form()], detail_type: Annotated[str, Form()], token: str = Depends(oauth2_scheme)):
    print(f"detail_batch {detail_type}")
    user = decode_jwt(token)
    user_key = user["user"]
    with open("./user.json", 'r', encoding='utf-8') as file:
        # 解析文件内容到Python数据结构
        data = json.load(file)
        if user_key in data:
            rst = data[user_key]
            client = rst['client']
            targets_list = json.loads(targets)
            keys = []
            cnt = 2
            for target in targets_list:
                timestamp_ms = int(time.time() * 1000)
                chars = string.ascii_letters
                random_string = ''.join(random.choice(chars) for _ in range(length))
                key = f'{timestamp_ms}{random_string}'
                target["key"] = key
                fooocus.deal_cache[key] = {"finish": False, "progress": 0, "cnt": f"0/{cnt}"}
                keys.append(key)
            # detail_type 2 脸 3 手臂 4 腿 5 手 6 其他
            need_face = False
            out_prompts = "real photo"
            mode = 0
            detail_type = int(detail_type)
            if detail_type == 2:
                need_face = True
                out_prompts = None
                mode = 1
            if detail_type == 3 or detail_type == 4:
                mode = 1
                face_url = default_face
            if detail_type == 5 or detail_type == 6:
                mode = 0
                face_url = default_face

            thread = threading.Thread(target=batch, args=(targets_list, face_url, cnt, mode, out_prompts, need_face, client))
            thread.start()
            return {"code": 200, "data": {"keys": keys}}
        else:
            return {"code": 500, "data": {}}


def batch(targets_list, face_url, cnt, mode, out_prompts, need_face, client):
    print(f"out_prompts {out_prompts}")
    print(f"need_face {need_face}")
    print(f"mode {mode}")
    for target in targets_list:
        paint_url = target['pic_url']
        mask_url = target['mask_url']
        key = target['key']
        print(face_url)
        print(paint_url)
        print(mask_url)
        parsed_url = urlparse(face_url)
        path = parsed_url.path
        face_name = os.path.basename(path)
        cfg = face_config[face_name]
        if cfg is not None:
            prompts = cfg['prompts']
            if out_prompts is not None:
                prompts = out_prompts
            base_model = cfg['model']
            refiner_model = cfg['refiner_model']
            if not need_face:
                face_url = ""
            print(prompts)
            print(base_model)
            print(refiner_model)
            print(key)
            print(client)
            fooocus.generate_in_paint_mode(prompts, base_model, refiner_model, 0.6, paint_url, mask_url,
                                           face_url, mode, cnt, key, client)
        else:
            print(f"cfg not exist {face_name}")


@app.post("/swapface")
async def swap_face(paint_url: Annotated[str, Form()], mask_url: Annotated[str, Form()],
                    face_url: Annotated[str, Form()]):
    print(f"swap_face p {paint_url}")
    print(f"swap_face m {mask_url}")
    print(f"swap_face f {face_url}")
    parsed_url = urlparse(face_url)
    path = parsed_url.path
    face_name = os.path.basename(path)
    cfg = face_config[face_name]
    if cfg is not None:
        cnt = 4
        prompts = cfg['prompts']
        base_model = cfg['model']
        refiner_model = cfg['refiner_model']
        print(prompts)
        print(base_model)
        print(refiner_model)

        timestamp_ms = int(time.time() * 1000)
        chars = string.ascii_letters
        random_string = ''.join(random.choice(chars) for _ in range(length))
        key = f'{timestamp_ms}{random_string}'
        fooocus.deal_cache[key] = {"finish": False, "progress": 0, "cnt": f"0/{cnt}"}
        thread = threading.Thread(target=fooocus.generate_in_paint_mode, args=(
        prompts, base_model, refiner_model, 0.6, paint_url, mask_url, face_url, 0, cnt, key))
        thread.start()
        return {"code": 200, "data": {"key": key, "cnt": cnt}}
    else:
        return {"code": 500}


@app.post("/detail")
async def try_detail(paint_url: Annotated[str, Form()], mask_url: Annotated[str, Form()],
                     face_url: Annotated[str, Form()], detail_type: Annotated[str, Form()]):
    print(f"detail p {paint_url}")
    print(f"detail m {mask_url}")
    print(f"detail f {face_url}")
    print(f"detail detail_type {detail_type}")

    parsed_url = urlparse(face_url)
    path = parsed_url.path
    face_name = os.path.basename(path)
    cfg = face_config[face_name]
    if cfg is not None:
        cnt = 2
        base_model = cfg['model']
        refiner_model = cfg['refiner_model']
        print(base_model)
        print(refiner_model)
        # detail_type 2 脸 3 手臂 4 腿 5 手 6 其他
        timestamp_ms = int(time.time() * 1000)
        chars = string.ascii_letters
        random_string = ''.join(random.choice(chars) for _ in range(length))
        key = f'{timestamp_ms}{random_string}'
        fooocus.deal_cache[key] = {"finish": False, "progress": 0, "cnt": f"0/{cnt}"}
        thread = threading.Thread(target=fooocus.generate_in_paint_mode, args=(
            "real photo", base_model, refiner_model, 0.6, paint_url, mask_url, face_url, 1, cnt, key))
        thread.start()
        return {"code": 200, "data": {"key": key, "cnt": cnt}}
    else:
        return {"code": 500}
