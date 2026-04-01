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

    def generate(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        history: list[dict] | None = None,
    ) -> QueryResult:
        context = self._build_context(chunks)
        system_message = self._system_prompt()
        user_message = f"CONTEXT:\n{context}\n\nQUESTION: {query}"

        messages = [{"role": "system", "content": system_message}]

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": user_message})

        response = self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            messages=messages,
        )

        prompt_parts = [f"[SYSTEM]\n{system_message}"]
        if history:
            prompt_parts.extend(
                f"[{m['role'].upper()}]\n{m['content']}" for m in history
            )

        prompt_parts.append(f"[USER]\n{user_message}")
        full_prompt = "\n\n".join(prompt_parts)

        return QueryResult(
            answer=response.choices[0].message.content,
            retrieved_chunks=chunks,
            full_prompt=full_prompt,
        )

    def _system_prompt(self) -> str:
        return (
            "# Role and Objective\n"
            "Provide accurate, context-grounded research assistance in philosophy of science.\n"
            "# Instructions\n"
            "- Answer the user's questions using only the provided context.\n"
            "- Cite sources by referencing the paper title and publication year.\n"
            "- Do NOT hallucinate.\n"
            "## Guidelines\n"
            "- Pay close attention to publication years.\n"
            "- When relevant, note the chronological development of ideas and "
            "distinguish between an author's earlier and later positions.\n"
            "- If the context presents only one side of a debate, note that the retrieved "
            "sources may not represent all perspectives on the topic.\n"
            "- Present different positions on a topic where appropriate.\n"
            "- If the context does not contain enough information to answer the user's "
            "question, explicitly say so."
        )

    def _build_context(self, chunks: list[RetrievedChunk]) -> str:
        sections = []
        for chunk in chunks:
            year = f" ({chunk.publication_year})" if chunk.publication_year else ""
            header = f"[Source: {chunk.paper_title}{year}]"
            sections.append(f"{header}\n{chunk.content}")
        return "\n\n***\n\n".join(sections)
