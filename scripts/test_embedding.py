from dotenv import load_dotenv
import os
from src.infrastructure.embedding import OpenAIEmbeddingClient

load_dotenv()

client = OpenAIEmbeddingClient(api_key=os.getenv("OPENAI_API_KEY"))

embedding = client.embed("What is epistemic opacity?")
print(f"Dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
