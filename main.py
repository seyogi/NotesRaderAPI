from fastapi import FastAPI, File, UploadFile, Form
from starlette.middleware.cors import CORSMiddleware # 追加
import iidx_full
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/iidx/uploadtext/")
async def upload_text(text: str = Form(),Theme: str="NOTES",displayNum: int=10):
    return {"message": iidx_full.f(io.StringIO(text),Theme,displayNum)}

@app.post("/iidx/uploadfile/")
async def upload_file(file: UploadFile = File(...),Theme: str="NOTES",displayNum: int=10):
    return {"message": iidx_full.f(file.file,Theme,displayNum)}


#curl --noproxy 127.0.0.1 http://127.0.0.1:8000/iidx/?Theme=0
#uvicorn main:app
#space push