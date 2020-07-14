import pandas as pd


class CSVObserver:
    """
    an observer for the experiment results. will attach a time stamp to the data received and save it to a csv file
    """

    def __init__(self, result_location):
        self.result = result_location + '.csv'
        self.df = None
        self.started = False

    # gets a dictionary of values to save or a None value to stop listening
    def update(self, data):
        if data is None:
            self.df.to_csv(self.result, index=False)
            return
        # TODO add timeout

        if not self.started:
            self.started = True
            self.df = pd.DataFrame([data])
            return
        self.df = self.df.append([data], ignore_index=True)


class PlotObserver:
    """
    an observer for the experiment results. will attach a time stamp to the data received and return a data frame when asked
    """
    def __init__(self, df=None):
        self.df = df
        self.started = False

    # gets a dictionary of values to save or a None value to stop listening
    def update(self, data):
        if not self.started:
            self.started = True
            self.df = pd.DataFrame([data])
            return
        self.df = self.df.append([data], ignore_index=True)

    def get_dataframe(self):
        return self.df


class ConsoleObserver:
    """ an observer responsible for printing results to the screen"""

    def __init__(self):
        pass

    def update(self, data):
        if data is None:
            return
        print(data)
