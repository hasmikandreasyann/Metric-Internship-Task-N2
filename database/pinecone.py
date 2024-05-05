import pinecone

def init_pinecone():
    # Initialize Pinecone
    pinecone.init(api_key="your-pinecone-api-key", environment="us-west1-gcp")

    # Create or connect to an index
    index_name = "extracted-info"
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name)
    index = pinecone.Index(index_name)

    return index

index = init_pinecone()
