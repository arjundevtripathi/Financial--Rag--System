import re

class KPIExtractor:
    PATTERNS = {
        "revenue":          r"revenue[^\$]*\$?([\d,.]+\s*(?:billion|million|B|M)?)",
        "net_income":       r"net income[^\$]*\$?([\d,.]+\s*(?:billion|million|B|M)?)",
        "operating_income": r"operating income[^\$]*\$?([\d,.]+\s*(?:billion|million|B|M)?)",
        "gross_profit":     r"gross profit[^\$]*\$?([\d,.]+\s*(?:billion|million|B|M)?)",
        "debt":             r"(?:total )?debt[^\$]*\$?([\d,.]+\s*(?:billion|million|B|M)?)",
        "eps":              r"earnings per share[^\$]*\$?([\d,.]+)",
        "ebitda":           r"ebitda[^\$]*\$?([\d,.]+\s*(?:billion|million|B|M)?)",
    }

    @classmethod
    def extract(cls, text: str) -> dict:
        return {k: re.findall(p, text, re.IGNORECASE)[:3] for k, p in cls.PATTERNS.items()}

    @classmethod
    def summary(cls, text: str) -> str:
        metrics = cls.extract(text)
        lines = [f"{k.replace('_',' ').title()}: {v[0]}" for k, v in metrics.items() if v]
        return "\n".join(lines) or "No KPIs found."
