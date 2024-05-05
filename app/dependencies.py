import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

def init_pinecone():
    pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment='us-west1-gcp')
    if "vc_vectors" not in pinecone.list_indexes():
        pinecone.create_index("vc_vectors", dimension=768)  # Assuming 768-dim vectors from OpenAI
    return pinecone.Index("vc_vectors")
