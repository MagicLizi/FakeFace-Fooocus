import upyun_util
import fooocus
from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应更精确地设置
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)


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
    print(f"swap_face p {paint_url}")
    print(f"swap_face m {mask_url}")
    print(f"swap_face f {face_url}")
    cnt = 1
    result = fooocus.generate_in_paint_mode("", "copaxTimelessxlSDXL1_v11Lightning.safetensors",
                                            "realisticStockPhoto_v20.safetensors",
                                            0.6,
                                            paint_url,
                                            mask_url,
                                            face_url,
                                            0,
                                            cnt)
    print(result)
    return {"code": 200, "data": {"list": result}}


@app.post("/detail")
async def try_detail(paint_url: Annotated[str, Form()], mask_url: Annotated[str, Form()], face_url: Annotated[str, Form()], detail_type: Annotated[str, Form()]):
    print(f"detail p {paint_url}")
    print(f"detail m {mask_url}")
    print(f"detail m {face_url}")
    print(f"detail detail_type {detail_type}")
    cnt = 1
    # detail_type 2 脸 3 手臂 4 腿 5 手 6 其他
    result = fooocus.generate_in_paint_mode("real photo", "copaxTimelessxlSDXL1_v11Lightning.safetensors",
                                            "realisticStockPhoto_v20.safetensors",
                                            0.6,
                                            paint_url,
                                            mask_url,
                                            face_url,
                                            1,
                                            cnt)
    return {"code": 200, "data": {"list": result}}


@app.post('/test')
async def post_t():
    print("post t")
    return {"message": "test"}

