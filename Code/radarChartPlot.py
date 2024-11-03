import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def create_radar_chart(player1_data, player2_data, attributes):
    # Số lượng thuộc tính cần vẽ
    num_vars = len(attributes)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Hoàn thành vòng tròn
    player1_data = np.concatenate((player1_data, [player1_data[0]]))
    player2_data = np.concatenate((player2_data, [player2_data[0]]))
    angles += angles[:1]

    # Vẽ biểu đồ radar
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, player1_data, color='blue', alpha=0.25, label='Cầu thủ 1')
    ax.fill(angles, player2_data, color='orange', alpha=0.25, label='Cầu thủ 2')
    ax.set_yticklabels([])  # Ẩn nhãn trục y
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)
    plt.title('So sánh cầu thủ')
    plt.legend(loc='upper right')
    plt.show()

data = pd.read_csv('D:/results.csv')

player1_name = data['Player'].iloc[0]  # Cầu thủ đầu tiên trong danh sách
player2_name = data['Player'].iloc[1]  # Cầu thủ thứ hai trong danh sách
attributes = ['matches_played', 'minutes', 'starts', 'ProDist', 'TotDist_y', 'Live_x', 'Live_y', 'Touches', 'Def_3rd_y', 'Mn/Start', 'Rec', 'Carries', 'Cmp_y']

# Lấy dữ liệu cho từng cầu thủ
player1_data = data.loc[data['Player'] == player1_name, attributes].values.flatten()
player2_data = data.loc[data['Player'] == player2_name, attributes].values.flatten()

# Chuyển đổi sang kiểu float để đảm bảo tương thích với biểu đồ
create_radar_chart(np.array(player1_data, dtype=float), np.array(player2_data, dtype=float), attributes)
