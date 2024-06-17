import FinanceDataReader as fdr
import pandas as pd

class KrxCodes():

    def __init__(self):
        self.krx_filename = "./krx.csv"

        try:
            self.df_krx = pd.read_csv(self.krx_filename)
        except:
            self.df_krx = self.update()

    def update(self):
        df_krx = fdr.StockListing('KRX')
        df_krx.to_csv(self.krx_filename)
        return df_krx

    def convert_to_code(self, name):
        row = self.df_krx[self.df_krx.Name == name]
        if len(row) != 1:
            return ""
        else:
            return row['Code'].iloc[0]
        

#codeUtil = KrxCodes()
#ret = codeUtil.convert_to_code("SK텔레콤")
#print(ret)