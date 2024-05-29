from ProToolsData.ProToolsMarkerManager import ProToolsMarkerManager
from ProToolsData.ProToolsEDLManager import ProToolsEDLManager

class ProToolsDataManager:

    # ----------------------------------------------------------------------------
    # Create a ProToolsDataManager from a ProTools timecode file
    # filename: str    - the name of the file containing the Pro Tools Marker data
    # data_type: str   - the type of data to create
    ## returns: ProToolsDataManager
    @staticmethod
    def from_file(filename: str, data_type: str = "MRK") -> 'ProToolsDataManager':
        if data_type == "MRK":
            return ProToolsMarkerManager.from_file(filename)
        elif data_type == "EDL":
            return ProToolsEDLManager.from_file(filename)
        else:
            raise ValueError(f"Error: Invalid data type: {data_type}")
    # ----------------------------------------------------------------------------