import os

def enrich_metadata(chunks):
    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown")
        filename = os.path.basename(source)
        parts = filename.replace(".pdf","").replace(".txt","").split("_")
        chunk.metadata["company"]     = parts[0] if parts else "unknown"
        chunk.metadata["fiscal_year"] = parts[1] if len(parts) > 1 else "unknown"
        chunk.metadata["filename"]    = filename
    return chunks
