import filecmp
import sys
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")

import unittest
from Scripts.CaptionMaker import SRTMaker
from Scripts.LanguageSpecificPunctuationPriority import generate_languages2
import os

class TestSRTMaker(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.LANGUAGES = generate_languages2()
        self.ALPHA_TYPES = ["Arabic", "Armenian", "Balbodh", "Brahmi", "Cyrillic", "Etheopic", "Gurmukhi", "Hangeul", "Latin", "Mon", "Tibetan"]

    def test_create_captions(self):
        path = "/Volumes/VONLivingDead/~Internal Software/Captioning Test Cases"
        for alphabet_type in self.ALPHA_TYPES:
            alphabet_folder = path + f"/{alphabet_type} Script Languages"
            if os.path.exists(alphabet_folder):
                for lang in os.listdir(alphabet_folder):
                    with self.subTest(lang=lang):
                        print(f"Testing {lang}")
                        testcase = "01"
                        project_path = alphabet_folder + f"/{lang}/{self.LANGUAGES[lang]}_TestCase{testcase}/{self.LANGUAGES[lang]}_TestCase{testcase}_" + "{type}.{format}"

                        translation_path = project_path.format(type="Script", format="docx")
                        timecode_path = project_path.format(type="Timecode", format="txt")
                        srt_path = project_path.format(type="Output", format="srt")
                        expected_path = project_path.format(type="Expected", format="srt")

                        srt_maker = SRTMaker(translation_path, timecode_path, expected_path, self.LANGUAGES[lang])
                        srt_maker.create_captions(split=True)
                        # self.assert_(filecmp.cmp(srt_path, expected_path, shallow=False), f"Failed {lang} test case {testcase}")

if __name__ == '__main__':
    unittest.main()