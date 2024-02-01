class SRTInfo:
    def __init__(self, index, start_time, end_time, text):
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def __str__(self):
        return f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.text}\n"
    