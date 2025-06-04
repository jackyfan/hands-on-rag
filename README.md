# HANDS-ON-RAG 动手学RAG
## 安装环境
1. 安装python 
```bash
conda create -n hands-on-rag python=3.12.1
conda activate hands-on-rag
```
2. 安装向量数据库Chroma
```bash
pip install chromadb
```
 测试Chroma

 2.1 嵌入式的使用方式
```python
import chromadb 
client = chromadb.PersistentClient(path="./chroma_db") 
client.heartbeat()
```
 2.2 启动C/S模式
```bash
chroma run --path ./chroma_db 
```
成功提示以下信息
```bash
Running Chroma 
Saving data to: ./chroma_db 
Connect to chroma at: http://localhost:8000
```
进入客户端测试
```python
import chromadb 
chroma_client = chromadb.HttpClient(host='localhost', port=8000) 
chroma_client.heartbeat() 
```

3. 安装LlamaIndex
```bash
pip install llama-index
```
安装ollama模型库
```bash
pip install llama-index-llms-ollama 
```
安装ollama嵌入模型库
```bash
pip install llama-index-embeddings-ollama
```

4. 下载安装Ollama
下载地址：https://ollama.com/download
5. 部署大模型
```bash
ollama run qwen3:0.6b
```
部署嵌入模型
```bash
ollama pull milkey/dmeta-embedding-zh:f16
ollama serve
```
