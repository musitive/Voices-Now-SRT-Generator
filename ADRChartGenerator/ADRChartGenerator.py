import csv
import re
from Scripts.Script import Script

# ================================================================================================

WIDTH = 22

# ================================================================================================

class ADRChartGenerator:
    # ----------------------------------------------------------------------------
    def __init__(self, lds_script: Script):
        self.lds_script = lds_script
        self.character_dict = {}
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Iterate through the script and store the character and loop number in a dictionary
    ## return: None
    def iterate(self) -> None:
        for loop, block in self.lds_script.blocks.items():
            # Get the character name
            character = block.character
            character = re.sub(r'\s*\([^)]*\)', '', character)  # Remove "(*)" format

            # Check if the character is in the dictionary
            if character not in self.character_dict:
                self.character_dict[character] = []
            
            # Add the loop number to the character's list
            self.character_dict[character].append(loop)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Generate a CSV file from the character_dict
    # filename: str   - the name of the CSV file
    ## return: None
    def generate_csv(self, filename: str) -> None:
        # Open the CSV file and create a writer
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Iterate through the character_dict and write to the CSV file
            for character, loop_numbers in self.character_dict.items():
                n = len(loop_numbers)

                # Split the loop numbers into rows of WIDTH
                if n > WIDTH:   # If the number of loop numbers is greater than WIDTH
                    number_of_rows = n // WIDTH

                    # Iterate through rows of length width
                    for i in range(number_of_rows):
                        start = i * WIDTH
                        end = (i+1) * WIDTH
                        row = [character] + loop_numbers[start:end]

                        writer.writerow(row)
                        character = ''  # Empty character for subsequent rows
                    
                    # Write the remaining loop numbers
                    row = [character] + loop_numbers[number_of_rows * WIDTH:]
                    writer.writerow(row)

                else:   # If the number of loop numbers is less than or equal to WIDTH
                    row = [character] + loop_numbers
                    writer.writerow(row)
    # ----------------------------------------------------------------------------

# ==============================================================================
