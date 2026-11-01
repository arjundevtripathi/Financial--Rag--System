from openai import OpenAI
from src.utils.config import OPENAI_API_KEY, MODEL_NAME
from src.llm.prompt_template import FINANCIAL_RAG_PROMPT
from src.utils.logger import logger

class ResponseGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate(self, question: str, docs: list) -> str:
        context = "\n\n---\n\n".join([
            f"[Source: {doc.metadata.get('source','unknown')} | "
            f"Company: {doc.metadata.get('company','unknown')}]\n{doc.page_content}"
            for doc in docs
        ])
        prompt = FINANCIAL_RAG_PROMPT.format(context=context, question=question)
        logger.info(f"Generating answer for: {question[:60]}")
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content
