from pathlib import Path
from src.parser import extract_text, ResumeParseError

for pdf in Path("data/test_resumes").glob("*.pdf"):
    print("=" * 60)
    print(pdf.name)
    try:
        text = extract_text(pdf.read_bytes())
        print(text[:800])
    except ResumeParseError as e:
        print("ERROR:", e)