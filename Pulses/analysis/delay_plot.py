import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../experiment/delay.csv')
sns.scatterplot(data=df, x='units(LC)', y='delay(us)')
plt.show()
