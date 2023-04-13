from fastapi import FastAPI, File, UploadFile, HTTPException, status, Form
from starlette.middleware.cors import CORSMiddleware # 追加
import iidx_full

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List
from pydantic import BaseModel
import shutil
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
async def upload_text(text: str = Form(),Theme: str="NOTES"):
    return {"message": iidx_full.f(io.StringIO(text),Theme)}

@app.post("/iidx/uploadfile/")
async def upload_file(file: UploadFile = File(...),Theme: str="NOTES"):
    tmp_path: Path = ""
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)
    except Exception as e:
        print(f"一時ファイル作成: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="一時ファイル作成できません",
        )
    finally:
        file.file.close()
        
    csv_file = open(tmp_path, "r", encoding="utf-8", errors="", newline="" )
    #csv_file.close()
    return {"message": iidx_full.f(csv_file,Theme)}


#curl --noproxy 127.0.0.1 http://127.0.0.1:8000/iidx/?Theme=0
#uvicorn main:app