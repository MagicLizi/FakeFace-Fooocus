from fastapi import FastAPI
import upyun_util
import fooocus
from fastapi import Request

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


@app.post("/swapbg")
async def swap_bg(request: Request):
    print("swap_bg")

@app.post("/swapface")
async def swap_face(request: Request):
    data = await request.json()
    paint_url = data.paint_url
    mask_url = data.mask_url
    face_url = data.face_url
    cnt = 8
    result = fooocus.generate_in_paint_mode("", "copaxTimelessxlSDXL1_v11Lightning.safetensors",
                                            "realisticStockPhoto_v20.safetensors",
                                            0.6,
                                            paint_url,
                                            mask_url,
                                            face_url,
                                            0,
                                            cnt)


@app.post("/detailface")
async def detail_face(request: Request):
    data = await request.json()
    paint_url = data.paint_url
    mask_url = data.mask_url
    face_url = data.face_url
    cnt = 5
    result = fooocus.generate_in_paint_mode("", "copaxTimelessxlSDXL1_v11Lightning.safetensors",
                                            "realisticStockPhoto_v20.safetensors",
                                            0.6,
                                            paint_url,
                                            mask_url,
                                            face_url,
                                            1,
                                            cnt)


@app.post("/detailarm")
async def detail_arm(request: Request):
    print("detail_arm")


@app.post("/detailleg")
async def detail_leg(request: Request):
    print("detail_leg")


@app.post("/detailhand")
async def detail_hand(request: Request):
    print("detail_hand")


@app.post("/detailothers")
async def detail_others(request: Request):
    print("detail_others")

