import gradio as gr
from src.services.query import QueryService


class GradioApp:
    def __init__(self, query_service: QueryService):
        self._query_service = query_service

    def _handle_query(self, question: str) -> tuple[str, str, str]:
        result = self._query_service.query(question)

        chunks_md = "".join(
            f"**{chunk.paper_title}** (score: {chunk.similarity_score:.3f})\n\n"
            f"{chunk.content[:300]}...\n\n---\n\n"
            for chunk in result.retrieved_chunks
        )

        prompt_md = f"```\n{result.full_prompt}\n```"

        return result.answer, chunks_md, prompt_md

    def build(self) -> gr.Blocks:
        with gr.Blocks(title="Logos") as app:
            gr.Markdown("# Logos\nA RAG research assistant for philosophy of science.")

            question = gr.Textbox(
                label="Question", placeholder="e.g. What is epistemic opacity?"
            )
            submit = gr.Button("Ask")
            answer = gr.Markdown(label="Answer")

            with gr.Accordion("Retrieved Chunks", open=False):
                chunks_display = gr.Markdown()

            with gr.Accordion("Full Prompt", open=False):
                prompt_display = gr.Markdown()

            submit.click(
                fn=self._handle_query,
                inputs=[question],
                outputs=[answer, chunks_display, prompt_display],
            )

            question.submit(
                fn=self._handle_query,
                inputs=[question],
                outputs=[answer, chunks_display, prompt_display],
            )

        return app
