from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.scrape import search_query
from models.scrape import file_detail
import uvicorn
import json
import os
app = FastAPI()
if os.environ.get("VERCEL") == "1":
    uvicorn.run(app, host="0.0.0.0", port=8080)
@app.get("/search")
def read_item(q: str):
    search = search_query(q)
    try:
        results = search.get_search()
        return json.loads(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/")
def read_root():
    return {"Detail": "This API is part of my side project java application named World Library developed by Boon Jefferson Brigoli."}
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