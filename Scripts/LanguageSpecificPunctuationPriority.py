import csv

PRIORITY_BY_LANGUAGE = {
    "ENG": "(\.\s+)|[\!\?\;]|[\,\:\—]|\s",
    "BIS": "(\.\s+)|[\?\;]|[\,\:\—]|\s",

    # Arabic punctuation marks:
    # U+06D4 ۔ ARABIC FULL STOP
    # U+061F ؟ ARABIC QUESTION MARK
    # U+061B ؛ ARABIC SEMICOLON
    # U+060C ، ARABIC COMMA
    "ARA": "(\.\s+)|[\!\u06D4\u061F\u061B]|[\u060C\:\—]|\s",
    "FAR": "(\.\s+)|[\!\u06D4\u061F\u061B]|[\u060C\:\—]|\s",
    "URD": "(\.\s+)|[\!\u061F\u061B]|[\u060C\:\—]|\s",      # removed arabic full stop because it is in the middle of a word

    # Chinese punctuation marks:
    # U+3002 。 IDEOGRAPHIC FULL STOP
    # U+FF1F ？ FULLWIDTH QUESTION MARK
    # U+FF01 ！ FULLWIDTH EXCLAMATION MARK
    # U+FF0C ， FULLWIDTH COMMA
    # U+FF1A ： FULLWIDTH COLON
    "YUE": "(\u3002\s+)|[\uFF1F\uFF01]|[\uFF0C\uFF1A\—]|\s",
    "CMN": "(\u3002\s+)|[\uFF1F\uFF01]|[\uFF0C\uFF1A\—]|\s",
    "JPN": "(\u3002\s+)|[\uFF1F\uFF01]|[\uFF0C\uFF1A\—]|\s",

    # Amharic punctuation marks:
    # U+1362 ። ETHIOPIC FULL STOP
    # U+1367 ፧ ETHIOPIC QUESTION MARK
    # U+1364 ፤ ETHIOPIC COLON
    # U+1368 ፨ ETHIOPIC PARAGRAPH SEPARATOR
    # U+1363 ፣ ETHIOPIC COMMA
    # U+1365 ፥ ETHIOPIC SEMICOLON
    "AMH": "(\u1362\s+)|[\!\?\u1367\u1364\u1368]|[\u1363\u1365\—]|\s",

    # Armenian punctuation marks:
    # U+0589 ։ ARMENIAN FULL STOP
    # U+055C ՜ ARMENIAN EXCLAMATION MARK
    # U+055E ՞ ARMENIAN QUESTION MARK
    # U+055D ՝ ARMENIAN COMMA
    # U+2024 ․ ONE DOT LEADER
    "HYE": "(\u0589\s+)|(\:\s+)|[\u055C\u055E\u055D]|[\,\.\u2024\—]|\s",
}

def generate_languages() -> dict:
    languages = {}
    with open('/Users/studiod/Documents/GitHub/Voices-Now-SRT-Generator/Scripts/All_Languages.csv', 'r') as file:
        reader = csv.reader(file)
        languages = {lang[1].upper(): lang[2] for lang in reader}
    return languages