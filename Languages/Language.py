
# Errors
INVALID_CHAR_COUNT = "Error: Max character count {0} must be greater than 0"
INVALID_CODE_LENGTH = "Error: Language code {0} must be 3 characters"
INVALID_CODE_FORMAT = "Error: Language code {0} must be uppercase"

def validate_language_code(code: str) -> None:
    """Validate the language code"""
    # assert len(code) == 3, INVALID_CODE_LENGTH.format(code)
    assert code.isupper(), INVALID_CODE_FORMAT.format(code)

class Language:
    def __init__(self, id: str, code: str, name: str, script_type: str,
                    supports_split: bool, max_char_count: int):
        """Language subclass to store language information"""
        
        validate_language_code(code)
        assert max_char_count > 0, INVALID_CHAR_COUNT.format(max_char_count)

        self.id = id
        self.code = code
        self.name = name
        self.script_type = script_type
        self.supports_split = supports_split
        self.max_char_count = max_char_count