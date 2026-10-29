import pandas as pd


df = pd.read_csv("../dataset/bot_detection_data.csv")


print(df.head())

print("\nDataset Shape:")
print(df.shape)


print("\nLabel Distribution:")
print(df["Bot Label"].value_counts())


print("\nBot Samples:")
print(df[df["Bot Label"]==1]["Tweet"].head(10))


print("\nHuman Samples:")
print(df[df["Bot Label"]==0]["Tweet"].head(10))