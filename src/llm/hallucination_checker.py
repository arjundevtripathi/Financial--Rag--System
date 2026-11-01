from openai import OpenAI
from src.utils.config import OPENAI_API_KEY
from src.llm.prompt_template import HALLUCINATION_PROMPT

class HallucinationChecker:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def check(self, question: str, context: str, answer: str) -> str:
        prompt = HALLUCINATION_PROMPT.format(
            question=question, context=context, answer=answer)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
