import csv
import re
from Scripts.Script import LdsScript

WIDTH = 22

class ADRChartGenerator:
    def __init__(self, ldsscript):
        self.ldsscript = ldsscript
        self.character_dict = {}


    """
    Iterate through the script and store the character and loop number in a dictionary
    """
    def iterate(self):
        for loop, block in self.ldsscript.blocks.items():
            character = block.character
            character = re.sub(r'\s*\([^)]*\)', '', character)  # Remove "(*)" format

            if character not in self.character_dict:
                self.character_dict[character] = []
            self.character_dict[character].append(loop)


    """
    Generate a CSV file from the character_dict
    filename: str   - the name of the CSV file
    """
    def generate_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for character, loop_numbers in self.character_dict.items():
                c=character
                n=len(loop_numbers)
                if n>WIDTH:
                    m=n//WIDTH
                    for i in range(m):
                        writer.writerow([c] + loop_numbers[i*WIDTH:(i+1)*WIDTH])
                        c=''
                    writer.writerow([c] + loop_numbers[m*WIDTH:])
                else:
                    writer.writerow([c] + loop_numbers)

# Test Case
if __name__ == '__main__':
    # Example usage
    script = LdsScript('tests/BMVL_508_PD80000816_SCR_IND-INDONESIAN.docx')
    iterator = ADRChartGenerator(script)
    iterator.iterate()
    iterator.generate_csv('tests/BMVL_508_IND.csv')