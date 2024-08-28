
from fastapi import FastAPI, HTTPException
from models.scrape import Query
from models.scrape import file_detail
import requests
import uvicorn
import json
app = FastAPI()
@app.get("/")
async def read_root():
    return {"Detail": "This API is part of a side project for java application named World Library and is developed by Boon Jefferson Brigoli.","Debug function":"/debug"}
@app.get("/search")
def read_item(q: str):
    search = Query(q)
    try:
        results = search.get_result(debug=True)
        return json.loads(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/detail")
def get_item_detail(file_link):
    return file_detail.get_file_detail()
@app.get("/download")
def download(url:str):
    try:
        file = file_detail.download(url)
        response = requests.get(file, stream=True)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/debug")
def debug():
    return Query(q='').debug()
@app.get("/v2/search")
def search(*params):
    return None