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

        llm_response = result.llm_response
        answer = llm_response.answer

        # format citations
        if llm_response.citations:
            citations_md = "\n".join(
                f'- {c.authors} ({c.year}) — "{c.title}"'
                if c.year
                else f'- {c.authors} — "{c.title}"'
                for c in llm_response.citations
            )
            answer += f"\n\n**Sources:**\n{citations_md}"

        # add caveat if present
        if llm_response.caveat:
            answer += f"\n\n> **Note:** {llm_response.caveat}"

        chat_history = chat_history + [{"role": "assistant", "content": answer}]

        history_state = history_state + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": llm_response.answer},
        ]

        chunks_md = "".join(
            f"**{chunk.paper_title}** (score: {chunk.similarity_score:.3f})\n\n"
            f"{chunk.content[:300]}...\n\n---\n\n"
            for chunk in result.retrieved_chunks
        )

        prompt_md = f"```\n{result.full_prompt}\n```"

        return chat_history, history_state, chunks_md, prompt_md

    def _clear_conversation(self):
        return (
            [
                {
                    "role": "assistant",
                    "content": "Ask me about epistemic opacity, the use of AI in science, or any other related topic.",
                }
            ],
            [],
            "",
            "",
        )

    def _build_theme(self) -> gr.themes.Soft:
        return gr.themes.Soft(
            primary_hue=gr.themes.Color(
                c50="#f5f3ff",
                c100="#ede9fe",
                c200="#ddd6fe",
                c300="#c4b5fd",
                c400="#a78bfa",
                c500="#7f77dd",
                c600="#534ab7",
                c700="#4c3daa",
                c800="#3f3291",
                c900="#352b78",
                c950="#221b54",
            ),
            font=("Georgia", "serif"),
            font_mono=("Menlo", "monospace"),
        )

    def build(self) -> gr.Blocks:
        theme = self._build_theme()

        with gr.Blocks(
            title="Logos",
            theme=theme,
        ) as app:
            gr.Image(
                "logo.svg",
                show_label=False,
                container=False,
                height=321,
                interactive=False,
            )

            chatbot = gr.Chatbot(
                show_label=False,
                height=350,
                value=[
                    {
                        "role": "assistant",
                        "content": "Ask me about epistemic opacity, the use of AI in science, or any other related topic.",
                    }
                ],
            )
            history_state = gr.State([])

            with gr.Row():
                question = gr.Textbox(
                    label="Question",
                    placeholder="e.g. What is epistemic opacity?",
                    scale=4,
                )
                submit = gr.Button("Ask", scale=1)

            clear = gr.Button("Clear Conversation", variant="secondary")

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

            clear.click(
                fn=self._clear_conversation,
                outputs=[chatbot, history_state, chunks_display, prompt_display],
            )

        return app
