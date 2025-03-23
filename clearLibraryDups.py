import json

def remove_duplicates(json_data):
    seen = set()
    unique_data = {}
    
    for book, puzzles in json_data.items():
        unique_puzzles = []
        for puzzle in puzzles:
            key = (puzzle["numbers"], puzzle["operators"])
            if key not in seen:
                seen.add(key)
                unique_puzzles.append(puzzle)
        unique_data[book] = unique_puzzles
    
    return unique_data

# Beispiel: JSON aus einer Datei laden
with open("library.json", "r", encoding="utf-8") as file:
    data = json.load(file)

cleaned_data = remove_duplicates(data)

# Bereinigte JSON-Datei speichern
with open("library_cleaned.json", "w", encoding="utf-8") as file:
    json.dump(cleaned_data, file, indent=4, ensure_ascii=False)
