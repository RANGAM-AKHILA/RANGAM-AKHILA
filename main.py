import shutil
import subprocess
from pathlib import Path
from praatio import textgrid

# =========================================================
# USER CONFIGURATION
# =========================================================
CORPUS_DIR = Path(r"C:\Users\ranga\Downloads\Assignment\Assignment\mfa_corpus\speaker1")
OUTPUT_DIR = Path(r"C:\Users\ranga\Downloads\Assignment\Assignment\mfa_output")

DICTIONARY = "english_us_arpa"
ACOUSTIC_MODEL = "english_us_arpa"
MFA_CMD = ["mfa"]

# =========================================================
# SETUP
# =========================================================
OUTPUT_DIR.mkdir(exist_ok=True)

TEMP_DIR = Path("temp_mfa_run")
if TEMP_DIR.exists():
    shutil.rmtree(TEMP_DIR)
TEMP_DIR.mkdir()

# Copy WAV + TXT
for f in CORPUS_DIR.glob("*"):
    shutil.copy(f, TEMP_DIR)

# =========================================================
# RUN MFA ALIGNMENT
# =========================================================
print("\n🔹 Running MFA alignment...\n")

subprocess.run([
    *MFA_CMD,
    "align",
    str(TEMP_DIR),
    DICTIONARY,
    ACOUSTIC_MODEL,
    str(OUTPUT_DIR),
    "--clean"
], check=True)

print("✅ MFA alignment completed")

# =========================================================
# FUNCTION TO WRITE PRAAT-STYLE INTERVAL OUTPUT
# =========================================================
def write_intervals(tier, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for idx, (start, end, text) in enumerate(tier.entries, start=1):
            f.write(f"intervals [{idx}]:\n")
            f.write(f"    xmin = {start:.6f}\n")
            f.write(f"    xmax = {end:.6f}\n")
            f.write(f"    text = \"{text}\"\n\n")

# =========================================================
# PROCESS TEXTGRIDS
# =========================================================
for tg_path in OUTPUT_DIR.glob("*.TextGrid"):

    print(f"\n📄 Processing {tg_path.name}")

    tg = textgrid.openTextgrid(
        str(tg_path),
        includeEmptyIntervals=True
    )

    word_tier = tg.getTier("words")
    phone_tier = tg.getTier("phones")

    stem = tg_path.stem

    # -----------------------------------------------------
    # WORD INTERVALS (PRAAT STYLE)
    # -----------------------------------------------------
    word_out = OUTPUT_DIR / f"{stem}_words_intervals.txt"
    write_intervals(word_tier, word_out)

    # -----------------------------------------------------
    # PHONEME INTERVALS (PRAAT STYLE)
    # -----------------------------------------------------
    phone_out = OUTPUT_DIR / f"{stem}_phones_intervals.txt"
    write_intervals(phone_tier, phone_out)

    print(f"✔ Saved: {word_out.name}")
    print(f"✔ Saved: {phone_out.name}")

print("\n🎯 Praat-style interval output generated successfully.")
