import csv
import re
from Scripts.Script import LdsScript

class ADRChartGenerator:
    def __init__(self, ldsscript):
        self.ldsscript = ldsscript
        self.character_dict = {}

    def iterate(self):
        n = len(self.ldsscript.characters.cells)
        for i in range(1,n):
            loop_number = self.ldsscript.loops.cells[i].text
            character = self.ldsscript.characters.cells[i].text
            character = re.sub(r'\s*\([^)]*\)', '', character)  # Remove "(*)" format

            if character not in self.character_dict:
                self.character_dict[character] = []
            self.character_dict[character].append(loop_number)

    def generate_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Character', 'Loop Numbers'])
            for character, loop_numbers in self.character_dict.items():
                row = [character] + loop_numbers
                writer.writerow(row)

# Test Case
if __name__ == '__main__':
    # Example usage
    script = LdsScript('tests/BMVL_508_PD80000816_SCR_IND-INDONESIAN.docx')
    iterator = ADRChartGenerator(script)
    iterator.iterate()
    iterator.generate_csv('tests/BMVL_508_IND.csv')