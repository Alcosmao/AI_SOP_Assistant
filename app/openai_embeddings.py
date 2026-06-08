from openai import OpenAI
from app.config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def create_openai_embeddings(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )


    embedding = response.data[0].embedding

    return embedding