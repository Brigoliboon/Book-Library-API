from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.scrape import search_query
from models.scrape import file_detail
import uvicorn
import json
app = FastAPI()
@app.get("/search")
def read_item(q: str):
    search = search_query(q)
    try:
        results = search.get_search()
        return json.loads(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/download")
def download(url:str):
    try:
        file =file_detail.download(url)
        return json.loads(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))