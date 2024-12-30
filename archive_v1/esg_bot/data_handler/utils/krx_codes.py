import pandas as pd
import os

class KrxCodes:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_FILE_PATH = os.path.join(BASE_DIR, 'krx.csv')
        self.krx_filename = DATA_FILE_PATH

        try:
            self.df_krx = pd.read_csv(self.krx_filename)
        except:
            self.df_krx = self.update()

    def convert_to_code(self, name):
        row = self.df_krx[self.df_krx.Name == name]
        if len(row) != 1:
            return ""
        else:
            return row["Code"].iloc[0]


# codeUtil = KrxCodes()
# ret = codeUtil.convert_to_code("SK텔레콤")
# print(ret)