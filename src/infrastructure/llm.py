from openai import OpenAI
from src.domain.entities import RetrievedChunk, QueryResult
from src.domain.interfaces import LLMClient


class OpenAILLMClient(LLMClient):
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ):
        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    def generate(self, query: str, chunks: list[RetrievedChunk]) -> QueryResult:
        context = self._build_context(chunks)
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}",
                },
            ],
        )
        return QueryResult(
            answer=response.choices[0].message.content,
            retrieved_chunks=chunks,
        )

    def _system_prompt(self) -> str:
        return (
            "You are a research assistant for philosophy of science."
            "Answers the user's questions based only on the provided context."
            "Cite your sources by referencing the paper titles and the author."
            "If the context does not contain enough information to answer the user's question, then say so. Don't hallucinate."
        )

    def _build_context(self, chunks: list[RetrievedChunk]) -> str:
        sections = []
        for chunk in chunks:
            sections.append(f"[Source: {chunk.paper_title}]\n{chunk.content}")
        return "\n\n***\n\n".join(sections)
