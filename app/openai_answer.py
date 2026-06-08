from openai import OpenAI
from app.config import OPENAI_API_KEY, CHAT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def create_openai_answer(question, context, sources):
    system_prompt = (
        "You are a technical SOP assistant. "
        "Answer ONLY using the provided context. "
        "If the context is not enough, say: "
        "I don't know based on the provided document. "
        "Do not invent facts."       
    )
    user_prompt = (
        f"Question:\n{question}\n\n"
        f"Context:\n{context}\n\n"
        f"Sources:\n{sources}\n\n"
        "Write a clear grounded answer based only on the context above."
    )
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    answer = response.choices[0].message.content
    return answer