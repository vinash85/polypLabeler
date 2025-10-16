import json
import shutil
from pathlib import Path

QUESTIONS_PATH = Path(__file__).resolve().parents[1] / "questions.json"

def main() -> None:
    backup_path = QUESTIONS_PATH.with_suffix(".backup.json")
    shutil.copy2(QUESTIONS_PATH, backup_path)

    with open(QUESTIONS_PATH, "r") as rf:
        data = json.load(rf)

    jnet_options = ["Type1", "Type2A", "Type2B", "Type3", "None", "other"]

    for item in data:
        q1 = {
            "question": item.get("question"),
            "options": item.get("options", []),
        }
        q2 = {
            "question": "what is the JNET Class seen in this image?",
            "options": jnet_options,
        }
        item["questions"] = [q1, q2]

    with open(QUESTIONS_PATH, "w") as wf:
        json.dump(data, wf, indent=2)

    print(f"Updated {QUESTIONS_PATH} and created backup at {backup_path}")

if __name__ == "__main__":
    main()


