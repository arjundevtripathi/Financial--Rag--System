import re

class QueryProcessor:
    SYNONYMS = {
        "earnings": "net income earnings profit",
        "revenue":  "revenue sales turnover",
        "debt":     "debt liabilities borrowings",
        "growth":   "growth increase YoY year over year",
    }

    @classmethod
    def process(cls, query: str) -> str:
        return re.sub(r"\s+", " ", query.lower().strip())

    @classmethod
    def expand(cls, query: str) -> str:
        q = cls.process(query)
        for term, expansion in cls.SYNONYMS.items():
            if term in q:
                return f"{q} {expansion}"
        return q
