# ================================================================================================

# Dictionary of punctuation marks by alphabet script
# Punctuation marks are ordered by priority, from highest to lowest.
PRIORITY_BY_SCRIPT = {
    # --------------------------------------------------------------------------------
    # Latin script punctuation marks:
    "Latin": "(\.\s+)|[\!\?\;]|[\,\:\—]|\s",
    "Cyrillic": "(\.\s+)|[\!\?\;]|[\,\:\—]|\s",
    "Balbodh": "(\.\s+)|[\!\?\;]|[\,\:\—]|\s",
    "Mkhedruli": "(\.\s+)|[\!\?\;]|[\,\:\—]|\s",
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Arabic punctuation marks:
    # U+06D4 ۔ ARABIC FULL STOP
    # U+061F ؟ ARABIC QUESTION MARK
    # U+061B ؛ ARABIC SEMICOLON
    # U+060C ، ARABIC COMMA
    "Arabic": "(\.\s+)|[\!\u06D4\u061F\u061B]|[\u060C\:\—]|\s",
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Chinese punctuation marks:
    # U+3002 。 IDEOGRAPHIC FULL STOP
    # U+FF1F ？ FULLWIDTH QUESTION MARK
    # U+FF01 ！ FULLWIDTH EXCLAMATION MARK
    # U+FF0C ， FULLWIDTH COMMA
    # U+FF1A ： FULLWIDTH COLON
    "Chinese": "(\u3002)|[\uFF1F\uFF01]|[\uFF0C\uFF1A\—]",
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Ethiopic punctuation marks:
    # U+1362 ። ETHIOPIC FULL STOP
    # U+1367 ፧ ETHIOPIC QUESTION MARK
    # U+1364 ፤ ETHIOPIC COLON
    # U+1368 ፨ ETHIOPIC PARAGRAPH SEPARATOR
    # U+1363 ፣ ETHIOPIC COMMA
    # U+1365 ፥ ETHIOPIC SEMICOLON
    "Ethiopic": "(\u1362\s+)|[\?\u1367]|[\u1364\u1368\—]|\s",
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Armenian punctuation marks:
    # U+0589 ։ ARMENIAN FULL STOP
    # U+055C ՜ ARMENIAN EXCLAMATION MARK
    # U+055E ՞ ARMENIAN QUESTION MARK
    # U+055D ՝ ARMENIAN COMMA
    # U+2024 ․ ONE DOT LEADER
    "Armenian": "(\u0589\s+)|(\:\s+)|[\u055C\u055E\u055D]|[\,\.\u2024\—]|\s",
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Greek punctuation marks:
    # U+0387 · GREEK ANO TELEIA
    # U+00B7 · MIDDLE DOT
    "Greek": "(\.\s+)|[\!\;\u0387\u00B7]|[\,\:\—]|\s",
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Gurumukhi punctuation marks:
    # U+0964 । DEVANAGARI DANDA
    # U+0965 ॥ DEVANAGARI DOUBLE DANDA
    # U+0A4D ੍ GURMUKHI SIGN VIRAMA
    "Gurumukhi": "(\u0965\s+)|(\u0964\s+)|(\.\s+)|[\u0A4D\!\?\;]|[\,\:\—]|\s",
    "Malayalam": "(\u0965\s+)|(\u0964\s+)|(\.\s+)|[\!\?\;]|[\,\:\—]|\s",
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Brahmi punctuation marks:
    # U+11047 𑁇 BRAHMI DANDA
    # U+11048 𑁈 BRAHMI DOUBLE DANDA
    # U+11049 𑁉 BRAHMI PUNCTUATION DOT
    # U+1104A 𑁊 BRAHMI PUNCTUATION DOUBLE DOT
    # U+1104B 𑁋 BRAHMI PUNCTUATION LINE
    # U+1104C 𑁌 BRAHMI PUNCTUATION CRESCENT BAR
    # U+1104D 𑁍 BRAHMI PUNCTUATION LOTUS
    "Brahmi": "(\U0001104D\s+)|(\U0001104C\s+)|(\U0001104B\s+)|(\U0001104A\s+)|(\U00011049\s+)|(\U00011048\s+)|(\U00011047\s+)|\s",
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Burmese punctuation marks:
    # U+104A ၊ MYANMAR SIGN LITTLE SECTION
    # U+104B ။ MYANMAR SIGN SECTION
    # EM DASH is used as a colon
    # U+1038 း။ MYANMAR SIGN VISARGA
    # း။ is used as a question mark
    # U+104F ၏ MYANMAR SYMBOL GENITIVE
    # U+104D ၍ MYANMAR SYMBOL SHAN ONE
    "Burmese": "(\u104B\s+)|(\u104F\s+)|(\u104D\s+)|(\u1038\u104B)|(\-\u104A)|\s",
    # --------------------------------------------------------------------------------
}

# ================================================================================================

# Dictionary of punctuation marks by language
# Differs from PRIORITY_BY_SCRIPT by providing a more specific regex for each language
# Punctuation marks are ordered by priority, from highest to lowest.
PRIORITY_BY_LANGUAGE = {
    # --------------------------------------------------------------------------------
    # Latin script punctuation marks, removed exclamation mark due to being used in 
    # front and end of sentence
    "BIS": "(\.\s+)|[\?\;]|[\,\:\—]|\s",
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Arabic punctuation marks, removed arabic full stop because it is in the middle
    # of words
    "URD": "(\.\s+)|[\!\u061F\u061B]|[\u060C\:\—]|\s",
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Hebrew punctuation marks:
    # U+05C3 ׃ HEBREW PUNCTUATION SOF PASUQ
    "HEB": "(\.\s+)|(\:\s+)|(\u05C3\s+)|[\!\?\;]|[\,\:\—]|\s",
    # --------------------------------------------------------------------------------
}

# ================================================================================================