import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('D:/results.csv')
# Vẽ histogram cho toàn giải đấu

colum = [col for col in df.columns if col not in ['Player', 'Nation', 'Team', 'Pos', 'Age']]
for col in colum:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[col].dropna(), kde=True)  # 'dropna()' để bỏ các giá trị thiếu
    plt.title(f'Distribution of {col} for All Players')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.show()

# Vẽ histogram cho từng đội
for team, group in df.groupby('Team'):
    for col in colum:
        plt.figure(figsize=(10, 6))
        sns.histplot(group[col].dropna(), kde=True)
        plt.title(f'Distribution of {col} for Team {team}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.show()
