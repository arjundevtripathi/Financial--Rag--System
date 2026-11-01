"""Run: python -m src.evaluation.benchmark"""
from src.api.rag_pipeline import RAGPipeline

QUESTIONS = [
    "What was the total revenue?",
    "What was net income?",
    "What risks were mentioned?",
    "What are the debt obligations?",
    "Summarize the key business segments.",
    "What was earnings per share (EPS)?",
    "How did revenue change year over year?",
]

if __name__ == "__main__":
    pipeline = RAGPipeline()
    for q in QUESTIONS:
        print("=" * 60)
        print(f"Q: {q}")
        answer, sources = pipeline.ask(q)
        print(f"A: {answer[:400]}")
        print(f"Sources: {[s['source'] for s in sources]}")
