import os
import re
from tqdm import tqdm

input_dir = r"C:\Users\ranga\Downloads\Assignment\Assignment\transcripts"
output_dir = r"C:\Users\ranga\Downloads\Assignment\Assignment\para"

os.makedirs(output_dir, exist_ok=True)

index_pattern = re.compile(r"^\s*\d+\s*$")

for root, dirs, files in os.walk(input_dir):
    rel_path = os.path.relpath(root, input_dir)
    out_folder = os.path.join(output_dir, rel_path)
    os.makedirs(out_folder, exist_ok=True)

    for file in tqdm(files):
        if not file.endswith(".txt"):
            continue

        in_path = os.path.join(root, file)
        out_path = os.path.join(out_folder, file)

        with open(in_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        sentences = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if index_pattern.match(line):
                continue
            sentences.append(line)

        paragraph = " ".join(sentences)
        paragraph = re.sub(r"\s{2,}", " ", paragraph).strip()

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(paragraph)

        print("Exported", out_path)

print("Paragraph conversion complete")
print("Output saved in", output_dir)
