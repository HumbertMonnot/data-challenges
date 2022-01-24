import os
import pandas as pd


class Olist:
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        # Hints 1: Build csv_path as "absolute path" in order to call this method from anywhere.
            # Do not hardcode your path as it only works on your machine ('Users/username/code...')
            # Use __file__ instead as an absolute path anchor independant of your usename
            # Make extensive use of `breakpoint()` to investigate what `__file__` variable is really
        # Hint 2: Use os.path library to construct path independent of Mac vs. Unix vs. Windows specificities
        os.getcwd()
        csv_path = os.path.join("/Users/humbert/code/HumbertMonnot/data-challenges/04-Decision-Science/","data","csv")
        pd.read_csv(os.path.join(csv_path, 'olist_sellers_dataset.csv')).head()
        file_names = []
        for csv in os.listdir(csv_path):
            if csv[-4:]==".csv":
                file_names.append(csv)
        key_names = []
        for name in file_names:
            new_name = name
            if name[:6]=="olist_":
                new_name = new_name[6:]
            if name[-4:]==".csv":
                if name[-12:]=="_dataset.csv":
                    new_name = new_name[:-12]
                else :
                    new_name = new_name[:-4]
            key_names.append(new_name)
        data={}
        for name, file in zip(key_names, file_names):
            data[name]= pd.read_csv(os.path.join(csv_path, file))
        return data

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
