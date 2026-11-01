import pandas as pd
from langchain_core.documents import Document

def load_news(csv_path: str):
    df = pd.read_csv(csv_path)
    docs = []
    for _, row in df.iterrows():
        docs.append(Document(
            page_content=f"Headline: {row.get('headline', row.iloc[0])}",
            metadata={"date": str(row.get("date", "")), "type": "news", "source": "news.csv"},
        ))
    return docs
