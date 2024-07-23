
from fastapi import FastAPI, HTTPException
from models.scrape import Query
from models.scrape import file_detail
import uvicorn
import json
app = FastAPI()
@app.get("/")
async def read_root():
    return {"Detail": "This API is part of my side project java application named World Library developed by Boon Jefferson Brigoli."}
@app.get("/search")
def read_item(q: str):
    search = Query(q)
    try:
        results = search.get_result()
        return json.loads(results)
    except Exception as e:
        print(results)
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/detail")
def get_item_detail(file_link):
    return file_detail.get_file_detail()
@app.get("/download")
def download(url:str):
    try:
        file =file_detail.download(url)
        return json.loads(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))