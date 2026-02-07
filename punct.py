import os
import re
from tqdm import tqdm

INPUT_DIR = r"C:\Users\ranga\Downloads\Assignment\Assignment\para"
OUTPUT_DIR = r"C:\Users\ranga\Downloads\Assignment\Assignment\no_punct"

os.makedirs(OUTPUT_DIR, exist_ok=True)

WORD_PATTERN = re.compile(r"[A-Za-z']+[.,?]*")
NUMBER_PATTERN = re.compile(r"\d")
TIME_PATTERN = re.compile(r"^\d{1,2}:\d{2}$")

def normalize_apostrophes(text):
    return (
        text.replace("’", "'")
            .replace("‘", "'")
            .replace("`", "'")
            .replace("´", "'")
    )

def clean_token(token):
    token = normalize_apostrophes(token.lower())

    if TIME_PATTERN.fullmatch(token):
        return [token]

    token = re.sub(r"[^a-z0-9.,?:']", " ", token)

    parts = token.split()
    out = []

    for p in parts:
        if NUMBER_PATTERN.search(p):
            out.append(p)
        elif WORD_PATTERN.fullmatch(p):
            out.append(p)

    return out

def normalize_text(text):
    text = normalize_apostrophes(text)
    tokens = text.split()

    normalized = []
    for tok in tokens:
        normalized.extend(clean_token(tok))

    return " ".join(normalized)

def remove_outer_punctuation(text):
    cleaned = []

    for tok in text.split():
        tok = re.sub(r"^[.,?]+", "", tok)
        tok = re.sub(r"[.,?]+$", "", tok)
        if tok:
            cleaned.append(tok)

    return " ".join(cleaned)

def remove_numeric_outer_apostrophes(text):
    text = re.sub(r"(?<!\d)'(?=\d)", "", text)
    text = re.sub(r"(?<=\d)'(?!s)", "", text)
    return text

for root, _, files in os.walk(INPUT_DIR):
    for f in tqdm(files, desc="Normalizing paragraphs"):
        if not f.endswith(".txt"):
            continue

        in_path = os.path.join(root, f)
        rel = os.path.relpath(in_path, INPUT_DIR)
        out_path = os.path.join(OUTPUT_DIR, rel)

        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        with open(in_path, "r", encoding="utf-8") as r:
            text = r.read().strip()

        if not text:
            continue

        normalized = normalize_text(text)
        normalized = remove_outer_punctuation(normalized)
        normalized = remove_numeric_outer_apostrophes(normalized)

        with open(out_path, "w", encoding="utf-8") as w:
            w.write(normalized)
