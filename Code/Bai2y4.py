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

highest_counts = (team_means == team_means.max()).sum(axis=1)

# Tìm đội có nhiều chỉ số cao nhất
max_highest_count_team = highest_counts.idxmax()
max_count = highest_counts.max()

print(f"Đội có nhiều chỉ số cao nhất là: {max_highest_count_team} với {max_count} chỉ số.")