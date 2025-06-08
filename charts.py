import os 

class Charts:

    def __init__(self,data: dict):
        self.data = data
        self.size = self.terminal_size()

    def terminal_size(self):
        try:
            return os.get_terminal_size()
        except:
            return os.get_terminal_size((80,24))

    def bar(self, marker: str = "#"):

        if len(marker) > 1:
            raise Exception("Please only use a marker that is 1 in length!")

        if not self.data:
            return "No data"

        bargraph = "Temperature °C\n"

        for key, val in self.data.items():

            bargraph += f"{key} |{marker*val} \n"

        return bargraph



if __name__ == "__main__":
    chart = Charts(data = {"mon": 1, "tue":2, "wed":3,"thu":4,"fri":4,"sat":2,"sun":1})
    print(chart.bar(marker="+"))
    

