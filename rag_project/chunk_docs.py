"""
Step 2: Chunk the fetched documents using LangChain's text splitters.
Usage: python chunk_docs.py

Uses two LangChain splitters for comparison:
- RecursiveCharacterTextSplitter: general-purpose, tries paragraph/sentence
  boundaries first before falling back to a hard character cut.
- MarkdownHeaderTextSplitter: splits markdown specifically at ## headers,
  keeping each section intact.
"""

import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

RAW_DOCS_DIR = "raw_docs"
OUTPUT_FILE = "chunks.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
)


def recursive_chunks(text, source):
    """General-purpose chunking - works on any text (code, prose, etc)."""
    pieces = recursive_splitter.split_text(text)
    return [{"text": p, "source": source, "strategy": "recursive"} for p in pieces]


def markdown_chunks(text, source):
    """Markdown-aware chunking - splits at # / ## / ### headers."""
    docs = markdown_splitter.split_text(text)
    results = []
    for doc in docs:
        # doc.page_content is the section text; doc.metadata has header info
        content = doc.page_content
        # If a section is still very long, sub-chunk it with the recursive splitter
        if len(content) > CHUNK_SIZE * 2:
            results.extend(recursive_chunks(content, source))
        else:
            results.append({"text": content, "source": source, "strategy": "markdown_header"})
    return results


def main():
    all_recursive_chunks = []
    all_header_chunks = []

    for filename in os.listdir(RAW_DOCS_DIR):
        filepath = os.path.join(RAW_DOCS_DIR, filename)
        with open(filepath, "r", errors="ignore") as f:
            text = f.read()

        if not text.strip():
            continue

        all_recursive_chunks.extend(recursive_chunks(text, filename))

        if filename.endswith(".md"):
            all_header_chunks.extend(markdown_chunks(text, filename))
        else:
            # for non-markdown files (.py etc), fall back to recursive chunking
            all_header_chunks.extend(recursive_chunks(text, filename))

    print(f"Recursive chunking produced {len(all_recursive_chunks)} chunks")
    print(f"Markdown-header chunking produced {len(all_header_chunks)} chunks")

    with open(OUTPUT_FILE, "w") as f:
        json.dump({
            "fixed_size": all_recursive_chunks,   # keep key name for compatibility with later steps
            "markdown_header": all_header_chunks
        }, f, indent=2)

    print(f"Saved both chunk sets to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
