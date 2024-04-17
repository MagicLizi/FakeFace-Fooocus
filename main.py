from fastapi import FastAPI
import upyun_util
import fooocus

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


@app.post("/gen")
async def gen_fooocus_result():
    fooocus.generate_in_paint_mode("copaxTimelessxlSDXL1_v11Lightning.safetensors",
                                   "realisticStockPhoto_v20.safetensors",
                                   0.6,
                                   "https://files.magiclizi.com/fakeface/f2.png",
                                   "https://files.magiclizi.com/fakeface/mask.png",
                                   "https://files.magiclizi.com/fakeface/testface.png",
                                   0,
                                   1)

