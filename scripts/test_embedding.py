from src.config import Config

from src.infrastructure.embedding import OpenAIEmbeddingClient

config = Config.from_env()

client = OpenAIEmbeddingClient(config.openai_api_key)

embedding = client.embed("What is epistemic opacity?")
print(f"Dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
