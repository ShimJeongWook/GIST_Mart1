import pandas as pd
df = pd.read_excel("Goods.xlsx", engine = 'openpyxl')

for index, row in df.iterrows():
    print(str(row))