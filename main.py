import upyun_util
import fooocus
from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import json
from urllib.parse import urlparse
import os
import threading
import time
import random
import string

length = 10

app = FastAPI()

# app.mount("/", StaticFiles(directory="dist"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应更精确地设置
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

face_config = {}

with open("./ff.json", 'r', encoding='utf-8') as file:
    # 解析文件内容到Python数据结构
    data = json.load(file)
    for item in data:
        face_config[item['name']] = item

print(face_config)


@app.get('/')
async def root():
    return {"message": "index"}


@app.get("/library")
async def get_face_library(page: int = 1):
    if page < 1:
        return {"code": 500, "msg": "page Error Must >= 1"}
    else:
        rst_list = upyun_util.get_face_list("/fakeface/face")
        page_cnt = 30
        total_page = int(len(rst_list) / page_cnt)
        start = (page - 1) * page_cnt
        end = start + page_cnt
        sub_list = rst_list[start:end]
        return {"code": 200, "data": {"list": sub_list, "total_page": total_page}}


@app.get("/key")
async def get_key_cache(key: str = 1):
    if key in fooocus.deal_cache:
        rst = fooocus.deal_cache[key]
        # print(rst)
        return {"code": 200, "data": rst}
    else:
        return {"code": 500, "data": {}}


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
        cnt = 2
        prompts = cfg['prompts']
        base_model = cfg['model']
        refiner_model = cfg['refiner_model']
        print(prompts)
        print(base_model)
        print(refiner_model)
        # loop = asyncio.get_event_loop()

        timestamp_ms = int(time.time() * 1000)
        chars = string.ascii_letters
        random_string = ''.join(random.choice(chars) for _ in range(length))
        key = f'{timestamp_ms}{random_string}'
        fooocus.deal_cache[key] = {"finish":False,"progress":0, "cnt":f"0/{cnt}"}
        thread = threading.Thread(target=fooocus.generate_in_paint_mode, args=(prompts, base_model, refiner_model, 0.6, paint_url ,mask_url ,face_url, 0, cnt, key))
        thread.start()
        return {"code": 200, "data": {"key": key, "cnt":cnt}}
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
        # result = fooocus.generate_in_paint_mode("real photo", base_model,
        #                                         refiner_model,
        #                                         0.6,
        #                                         paint_url,
        #                                         mask_url,
        #                                         face_url,
        #                                         1,
        #                                         cnt)
        # print(result)
        # return {"code": 200, "data": {"list": result}}
        timestamp_ms = int(time.time() * 1000)
        chars = string.ascii_letters
        random_string = ''.join(random.choice(chars) for _ in range(length))
        key = f'{timestamp_ms}{random_string}'
        fooocus.deal_cache[key] = {"finish": False, "progress":0,"cnt":f"0/{cnt}"}
        thread = threading.Thread(target=fooocus.generate_in_paint_mode, args=(
        "real photo", base_model, refiner_model, 0.6, paint_url, mask_url, face_url, 1, cnt, key))
        thread.start()
        return {"code": 200, "data": {"key": key,"cnt":cnt}}
    else:
        return {"code": 500}
