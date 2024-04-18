import upyun_util
import fooocus
from typing import Annotated
from fastapi import FastAPI, Form
from urllib.parse import unquote, urlparse

app = FastAPI()


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
        total_page = int(len(rst_list)/page_cnt)
        start = (page - 1) * page_cnt
        end = start + page_cnt
        sub_list = rst_list[start:end]
        return {"code": 200, "data": {"list": sub_list, "total_page": total_page}}


@app.post("/swapface")
async def swap_face(paint_url: Annotated[str, Form()], mask_url: Annotated[str, Form()], face_url: Annotated[str, Form()]):
    cnt = 1
    result = fooocus.generate_in_paint_mode("", "copaxTimelessxlSDXL1_v11Lightning.safetensors",
                                            "realisticStockPhoto_v20.safetensors",
                                            0.6,
                                            paint_url,
                                            mask_url,
                                            face_url,
                                            0,
                                            cnt)
    return {"code": 200, "data": {"list": result}}


@app.post("/detail")
async def detail(paint_url: Annotated[str, Form()], mask_url: Annotated[str, Form()], face_url: Annotated[str, Form()], detail_type: Annotated[str, Form()]):
    cnt = 1
    # detail_type 0 脸 1 手臂 2 腿 3 膝盖 4 其他
    result = fooocus.generate_in_paint_mode("real photo", "copaxTimelessxlSDXL1_v11Lightning.safetensors",
                                            "realisticStockPhoto_v20.safetensors",
                                            0.6,
                                            paint_url,
                                            mask_url,
                                            face_url,
                                            1,
                                            cnt)
    return {"code": 200, "data": {"list": result}}

