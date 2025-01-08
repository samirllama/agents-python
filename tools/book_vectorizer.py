from typing import List, Dict

class BookVectorizer:
    def __init__(self, chunk_size=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[Dict]:
        chunks = []
        paragraphs = text.split('\n\n')
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += para + "\n\n"
            else:
                chunks.append(self._process_chunk(current_chunk))
                current_chunk = current_chunk[-self.overlap:] + para + "\n\n"

        if current_chunk:
            chunks.append(self._process_chunk(current_chunk))

        return chunks

    def _process_chunk(self, chunk: str) -> Dict:
        return {
            "text": chunk.strip(),
            "metadata": {
                "start_text": chunk[:100],
                "themes": self._detect_themes(chunk),
                "length": len(chunk)
            }
        }

    def _detect_themes(self, text: str) -> List[str]:
        # Simple keyword-based theme detection
        themes = []
        if any(word in text.lower() for word in ["virtue", "virtuous", "moral", "ethics"]):
            themes.append("virtue")
        if any(word in text.lower() for word in ["integrity", "honest", "truth"]):
            themes.append("integrity")
        return themes
