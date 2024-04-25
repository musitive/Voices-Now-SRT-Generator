import filecmp
import sys
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")

import unittest
from Scripts.CaptionMaker import SRTMaker
from Scripts.LanguageSpecificPunctuationPriority import generate_languages
import os

class TestSRTMaker(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.LANGUAGES = generate_languages()

    def test_create_captions(self):
        path = "/Volumes/VONLivingDead/~Internal Software/Captioning Test Cases"
        for lang in self.LANGUAGES:
            if os.path.exists(path + f"/{self.LANGUAGES[lang]}"):
                with self.subTest(lang=lang):
                    testcase = "01"
                    project_path = path + f"/{self.LANGUAGES[lang]}/{lang}_TestCase{testcase}/{lang}_TestCase{testcase}_" + "{type}.{format}"

                    translation_path = project_path.format(type="Script", format="docx")
                    timecode_path = project_path.format(type="Timecode", format="txt")
                    srt_path = project_path.format(type="Output", format="srt")
                    expected_path = project_path.format(type="Expected", format="srt")

                    srt_maker = SRTMaker(translation_path, timecode_path, srt_path, lang)
                    srt_maker.create_captions(split=True)
                    self.assert_(filecmp.cmp(srt_path, expected_path, shallow=False), f"Failed {lang} test case {testcase}")

if __name__ == '__main__':
    unittest.main()