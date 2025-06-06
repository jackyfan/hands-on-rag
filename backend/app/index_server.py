import os
import pickle
import chromadb
from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama

# 配置模型
llm_ollama = Ollama(model="qwen3:0.6b")
embedding_model = OllamaEmbedding(model_name="shaw/dmeta-embedding-zh")
Settings.llm = llm_ollama
Settings.embed_model = embedding_model
# 全局共享索引
index = None
# 存储上传的文档信息
stored_docs = {}
# 锁，对全局共享数据的互斥访问
lock = Lock()

# 索引持久化存储的位置
index_name = "./saved_index"
pkl_name = "stored_documents.pkl"
collection_name = "company_collection"
# 索引服务端口
SERVER_PORT = 5602

"""初始化向量索引"""


def init_index():
    global index, stored_docs
    chroma = chromadb.HttpClient(host="localhost", port=8000)
    collection = chroma.get_or_create_collection(name=collection_name)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    # 互斥访问
    with lock:
        # 存在就加载数据
        if os.path.exists(index_name):
            storage_context = StorageContext.from_defaults(persist_dir=index_name, vector_store=vector_store)
            index = load_index_from_storage(storage_context=storage_context)
        else:
            # 不存在，构造空的索引
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            index = VectorStoreIndex([], storage_context=storage_context)
            index.storage_context.persist(persist_dir=index_name)
        # 建已上传的文档信息从存储的文档中读取到内存
        if os.path.exists(pkl_name):
            with open(pkl_name, "rb") as f:
                stored_docs = pickle.load(f)


""""查询向量索引"""


def query_index(query_text):
    """"查询全局索引"""
    global index
    response = index.as_query_engine().query(query_text)
    return response


""""插入向量索引"""


def insert_index(doc_file_path, doc_id=None):
    global index, stored_docs
    document = SimpleDirectoryReader(input_files=[doc_file_path]).load_data()[0]
    if doc_id is not None:
        document.doc_id = doc_id
    with lock:
        index.insert(document)
        index.storage_context.persist(persist_dir=index_name)
        stored_docs[document.doc_id] = document.text[0:200]
        with open(pkl_name, "wb") as f:
            pickle.dump(stored_docs, f)
    return


"""获取文档清单"""


def get_document_list():
    global stored_docs
    document_list = []
    for doc_id, doc_text in stored_docs.items():
        document_list.append({"id": doc_id, "text": doc_text})
    return document_list


if __name__ == "__main__":
    print("initializing index...")
    init_index()

    print(f'Create server on {SERVER_PORT}...')
    # 构造多线程的管理器对象，设置监听端口和密码
    manager = BaseManager(('127.0.0.1', SERVER_PORT), b'password')
    # 注册函数
    print("Registering function...")
    manager.register('query_index', query_index)
    manager.register('insert_index', insert_index)
    manager.register('get_document_list', get_document_list)
    server = manager.get_server()
    # 启动服务
    print("Server started...")
    # 监听调用请求，产生一个新的处理线程
    server.serve_forever()
