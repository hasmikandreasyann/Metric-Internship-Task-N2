import pinecone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Initialize the Pinecone Index
def init_db():
    # Fetch the API key from environment variables
    api_key = os.getenv("PINECONE_API_KEY")
    pinecone.init(api_key=api_key, environment='us-west1-gcp')

    # Check if the index already exists, and create it if it does not
    if "vc_vectors" not in pinecone.list_indexes():
        # Create an index with a specific dimension
        # Note: Make sure the dimension matches the dimensionality of your vectors
        pinecone.create_index("vc_vectors", dimension=768)

    # Return a Pinecone Index object for operations
    return pinecone.Index("vc_vectors")


# Function to upsert vectors into the Pinecone database
def upsert_vector(vc_name, vector):
    # Initialize the Pinecone index
    index = init_db()

    # Upsert the vector under the specified name
    # The vc_name serves as a unique identifier for the vector in the index
    index.upsert(vectors=[(vc_name, vector)])


# Function to query for similar vectors
def query_similar_vectors(vector):
    # Initialize the Pinecone index
    index = init_db()

    # Query for top 3 similar vectors based on cosine similarity
    # Returns a list of similar vector IDs and their corresponding scores
    results = index.query(vector, top_k=3)
    return results
