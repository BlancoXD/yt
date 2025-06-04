import re
import unicodedata

def slugify(value):
    """
    Convert string to URL-friendly slug.
    """
    value = str(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)

def split_text(text, max_length=4000):
    """
    Splits long text into chunks under a max character count (e.g. for TTS limits).
    """
    chunks = []
    current_chunk = ""

    for sentence in text.split(". "):
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
