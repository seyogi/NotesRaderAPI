from fastapi import FastAPI, File, UploadFile, HTTPException, status
import iidx_full

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List
import shutil

app = FastAPI()
Theme_name = ['NOTES','PEAK','SCRATCH','SOF-LAN','CHARGE','CHORD']

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/iidx/")
def read_item(Theme: int=0):
    return iidx_full.f('7228-1124_sp_score.csv',Theme_name[Theme])

@app.post("/iidx/uploadfile/")
async def upload_file(file: UploadFile = File(...),Theme: int=0):
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
    return iidx_full.f(tmp_path,Theme_name[Theme])


#curl --noproxy 127.0.0.1 http://127.0.0.1:8000/iidx/?Theme=0