import os
from multiprocessing.managers import BaseManager
from werkzeug.utils import secure_filename
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()
# 启动CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = BaseManager(('127.0.0.1', 5602), b'password')
manager.register('query_index')
manager.register('insert_index')
manager.register('get_document_list')
manager.connect()


@app.get("/")
def home():
    return "Hello RAG."


""""异常处理函数"""


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(content="Invalid request parameters", status_code=400)


@app.get("/query")
def query_index(request: Request, query_text: str):
    global manager
    if query_text is None:
        return JSONResponse(content="No text found,please include a ?text=blah parameter in the URL", status_code=400)
    response = manager.query_index(query_text)._getvalue()
    response_json = {
        "text": str(response),
        "sources": [{"text": str(x.text),
                     "similarity": round(x.score, 2),
                     "doc_id": str(x.id_)} for x in response.source_nodes]
    }
    return JSONResponse(content=response_json, status_code=200)


@app.post("/uploadFile")
async def upload_file(request: Request, file: UploadFile = File(...), filename_as_doc_id: bool = False):
    global manager
    try:
        contents = await file.read()
        print("filename_as_doc_id：{}".format(str(filename_as_doc_id)))
        filepath = os.path.join('documents', file.filename)
        print("文件路径：{}".format(filepath))
        with open(filepath, "wb") as f:
            print("临时保存文件")
            f.write(contents)
        if filename_as_doc_id:
            print("新增索引：{}".format(file.filename))
            manager.insert_index(filepath, doc_id=file.filename)
        else:
            print("新增索引：{}".format(filepath))
            manager.insert_index(filepath)
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
            print("新增索引报错：{}".format(str(e)))
        return JSONResponse(content="Error:{}".format(str(e)), status_code=500)
    if os.path.exists(filepath):
        os.remove(filepath)
    return JSONResponse(content="File inserted", status_code=200)


@app.get("/getDocuments")
def get_documents(request: Request):
    document_list = manager.get_document_list()._getvalue()
    return JSONResponse(content=document_list, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5601)
