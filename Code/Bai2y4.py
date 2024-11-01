import pandas as pd

df = pd.read_csv('D:/results.csv')
# Vẽ histogram cho toàn giải đấu

colum = [col for col in df.columns if col not in ['Player', 'Nation', 'Team', 'Pos', 'Age']]
for col in colum:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')

# Tính trung bình của các chỉ số theo từng đội
team_means = df.groupby('Team')[colum].mean()

# Tìm đội có điểm số cao nhất cho mỗi chỉ số
top_teams = team_means.idxmax()

print("Đội có điểm số cao nhất ở mỗi chỉ số:")
top_teams.to_csv('D:/top_teams_test.csv', header=True)