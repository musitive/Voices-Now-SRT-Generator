import csv

PRIORITY_BY_SCRIPT = {
    "Latin": "(\.\s+)|[\!\?\;]|[\,\:\—]|\s",

    # Arabic punctuation marks:
    # U+06D4 ۔ ARABIC FULL STOP
    # U+061F ؟ ARABIC QUESTION MARK
    # U+061B ؛ ARABIC SEMICOLON
    # U+060C ، ARABIC COMMA
    "Arabic": "(\.\s+)|[\!\u06D4\u061F\u061B]|[\u060C\:\—]|\s",

    # Chinese punctuation marks:
    # U+3002 。 IDEOGRAPHIC FULL STOP
    # U+FF1F ？ FULLWIDTH QUESTION MARK
    # U+FF01 ！ FULLWIDTH EXCLAMATION MARK
    # U+FF0C ， FULLWIDTH COMMA
    # U+FF1A ： FULLWIDTH COLON
    "Chinese": "(\u3002\s+)|[\uFF1F\uFF01]|[\uFF0C\uFF1A\—]|\s",

    # Ethiopic punctuation marks:
    # U+1362 ። ETHIOPIC FULL STOP
    # U+1367 ፧ ETHIOPIC QUESTION MARK
    # U+1364 ፤ ETHIOPIC COLON
    # U+1368 ፨ ETHIOPIC PARAGRAPH SEPARATOR
    # U+1363 ፣ ETHIOPIC COMMA
    # U+1365 ፥ ETHIOPIC SEMICOLON
    "Ethiopic": "(\u1362\s+)|[\?\u1367]|[\u1364\u1368\—]|\s",

    # Armenian punctuation marks:
    # U+0589 ։ ARMENIAN FULL STOP
    # U+055C ՜ ARMENIAN EXCLAMATION MARK
    # U+055E ՞ ARMENIAN QUESTION MARK
    # U+055D ՝ ARMENIAN COMMA
    # U+2024 ․ ONE DOT LEADER
    "Armenian": "(\u0589\s+)|(\:\s+)|[\u055C\u055E\u055D]|[\,\.\u2024\—]|\s",
}

PRIORITY_BY_LANGUAGE = {
    # Latin script punctuation marks, removed exclamation mark due to being used in front and end of sentence
    "BIS": "(\.\s+)|[\?\;]|[\,\:\—]|\s",

    # Arabic punctuation marks, removed arabic full stop because it is in the middle of words
    "URD": "(\.\s+)|[\!\u061F\u061B]|[\u060C\:\—]|\s",

}

def generate_languages() -> dict:
    languages = {}
    with open('/Users/studiod/Documents/GitHub/Voices-Now-SRT-Generator/Scripts/All_Languages.csv', 'r') as file:
        reader = csv.reader(file)
        languages = {lang[1].upper(): lang[2] for lang in reader}
    return languages

def generate_script_type() -> dict:
    languages = {}
    with open('/Users/studiod/Documents/GitHub/Voices-Now-SRT-Generator/Scripts/All_Languages.csv', 'r') as file:
        reader = csv.reader(file)
        languages = {lang[1].upper(): lang[3] for lang in reader}
    return languages