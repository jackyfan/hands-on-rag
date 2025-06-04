import os
import pickle
import chromadb
from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from llama_index.core import Settings,SimpleDirectoryReader,VectorStoreIndex,StorageContext,load_index_from_storage
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama

