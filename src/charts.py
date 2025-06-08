import os 
import numpy as np

class Charts:

    def __init__(self,data: dict):
        self.data = data
        self.size = self.terminal_size()
        self.width = (self.size[0]//3)*2 - 10
        self.height = 18
        self.canvas = [[" " for _ in range(self.width)] for _ in range(self.height)]


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

        # lets get the y-axis 
        y_axis_points = [int(i) for i in list(np.linspace(0, self.height, 4))]

        for y in range(len(self.canvas)):
            
            reverse_idx = len(self.canvas)-1-y 

            if reverse_idx in y_axis_points:
                self.canvas[y][0] = f"{reverse_idx}" 

            else:
                self.canvas[y][0] = " " 

        # get points to pop our day labels
        label_points = [int(i) for i in list(np.linspace(0, self.width,9))]
        
        #plot points 
        
        for i in label_points[1:8]:
            self.canvas[5][i] = "+"


        
        bar_plot = "Weather Forecast (Temperature) \n"
        for y in range(self.height):
            bar_plot += "".join(self.canvas[y]) + "\n"
        
        x_axis = [" " for _ in range(self.width)]

        for idx in range(len(x_axis)):
            
            if idx == 0:
                pass 
            else:
                if idx in label_points:
                    x_axis[idx-1] = "d" 
                    x_axis[idx] = "a" 
                    x_axis[idx+1] = "y" 

        bar_plot += "".join(x_axis)





        return bar_plot

        

        


if __name__ == "__main__":
    chart = Charts(data = {"mon": 1, "tue":2, "wed":3,"thu":4,"fri":4,"sat":2,"sun":1})
    print(chart.bar())

