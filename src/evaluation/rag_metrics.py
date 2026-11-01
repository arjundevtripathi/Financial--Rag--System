"""RAG evaluation using RAGAS. Install: pip install ragas datasets"""
try:
    from ragas import evaluate
    from ragas.metrics import answer_relevancy, faithfulness, context_precision, context_recall
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

def evaluate_rag(questions, answers, contexts, ground_truths=None):
    if not RAGAS_AVAILABLE:
        print("Install ragas: pip install ragas datasets")
        return {}
    from datasets import Dataset
    data = {"question": questions, "answer": answers, "contexts": contexts}
    if ground_truths:
        data["ground_truth"] = ground_truths
    metrics = [answer_relevancy, faithfulness, context_precision]
    if ground_truths:
        metrics.append(context_recall)
    return evaluate(Dataset.from_dict(data), metrics=metrics)
