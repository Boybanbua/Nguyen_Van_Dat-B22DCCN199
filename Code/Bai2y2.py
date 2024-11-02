import pandas as pd

# Đọc file CSV và chuyển thành DataFrame
df = pd.read_csv('D:/results.csv')

colum = [col for col in df.columns if col not in ['Player', 'Nation', 'Team', 'Pos', 'Age']]
for col in colum:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')

# Tính toán cho toàn giải đấu
all_stats = pd.DataFrame(
    {f'Median of {col}': [round(df[col].median(), 2)] for col in colum}|
    {f'Mean of {col}': [round(df[col].mean(), 2)] for col in colum}|
    {f'Std of {col}': [round(df[col].std(), 2)] for col in colum}
    )
all_stats.insert(0, 'Team', 'all')

# Tính toán cho từng đội
team_stats = df.groupby('Team')[colum].agg(['median', 'mean', 'std']).reset_index()
team_stats = team_stats.round(2)

team_stats.columns = ['Team'] + [f'{stat.capitalize()} of {col}' for col in colum for stat in ['median', 'std', 'mean']]

# Kết hợp `all_stats` với `team_stats`
merged_df = pd.concat([all_stats, team_stats], ignore_index=True)

# Lưu kết quả vào file CSV
merged_df.to_csv('D:/results2.csv')