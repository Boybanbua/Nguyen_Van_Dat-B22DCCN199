import pandas as pd

# Đọc file CSV và chuyển thành DataFrame
df = pd.read_csv('D:/results.csv')

# Bỏ qua các chỉ số này
colum = [col for col in df.columns if col not in ['Player', 'Nation', 'Team', 'Pos', 'Age']]

# Chuyển đổi tất cả các cột chỉ số về kiểu số, nếu có lỗi chuyển đổi thì sẽ là NaN
for col in colum:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Tạo từ điển để lưu kết quả
top_players = {'Top 3 High': {}, 'Top 3 Low': {}}

for col in colum:
    # Bỏ qua cột nào có toàn giá trị NaN sau khi chuyển đổi
    if df[col].notna().sum() == 0:
        continue
    
    # Lấy top 3 cao nhất cho chỉ số
    top_high = df[['Player', col]].nlargest(3, col)

    # Lấy top 3 thấp nhất cho chỉ số
    top_low = df[['Player', col]].nsmallest(3, col)

    top_players['Top 3 High'][col] = top_high
    top_players['Top 3 Low'][col] = top_low