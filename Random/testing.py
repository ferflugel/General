import pandas as pd

df = pd.read_csv('words.txt', delim_whitespace=True)
print(df.head())
