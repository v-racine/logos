import gradio as gr
from src.services.query import QueryService


class GradioApp:
    def __init__(self, query_service: QueryService):
        self._query_service = query_service

    def _handle_query(
        self, message: str, chat_history: list[dict], history_state: list[dict]
    ) -> tuple[list[dict], list[dict], str, str]:

        if not message.strip():
            return chat_history, history_state, "", ""

        chat_history = chat_history + [{"role": "user", "content": message}]

        try:
            result = self._query_service.query(message, history=history_state)
        except Exception as e:
            # temporary message for local development
            error_msg = f"Something went wrong: {e}"
            chat_history = chat_history + [{"role": "assistant", "content": error_msg}]

            return chat_history, history_state, "", ""

        chat_history = chat_history + [{"role": "assistant", "content": result.answer}]

        history_state = history_state + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": result.answer},
        ]

        chunks_md = "".join(
            f"**{chunk.paper_title}** (score: {chunk.similarity_score:.3f})\n\n"
            f"{chunk.content[:300]}...\n\n---\n\n"
            for chunk in result.retrieved_chunks
        )

        prompt_md = f"```\n{result.full_prompt}\n```"

        return chat_history, history_state, chunks_md, prompt_md

    def build(self) -> gr.Blocks:
        with gr.Blocks(title="Logos") as app:
            gr.Markdown("# Logos\nA RAG research assistant for philosophy of science.")

            chatbot = gr.Chatbot(label="Conversation")
            history_state = gr.State([])

            with gr.Row():
                question = gr.Textbox(
                    label="Question",
                    placeholder="e.g. What is epistemic opacity?",
                    scale=4,
                )
                submit = gr.Button("Ask", scale=1)

            with gr.Accordion("Retrieved Chunks", open=False):
                chunks_display = gr.Markdown()

            with gr.Accordion("Full Prompt", open=False):
                prompt_display = gr.Markdown()

            submit.click(
                fn=self._handle_query,
                inputs=[question, chatbot, history_state],
                outputs=[chatbot, history_state, chunks_display, prompt_display],
            ).then(fn=lambda: "", outputs=[question])

            question.submit(
                fn=self._handle_query,
                inputs=[question, chatbot, history_state],
                outputs=[chatbot, history_state, chunks_display, prompt_display],
            ).then(fn=lambda: "", outputs=[question])

        return app
