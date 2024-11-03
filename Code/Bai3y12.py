import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
import seaborn as sns

data = pd.read_csv('D:/results.csv')
numeric_data = data.select_dtypes(include=[np.number]).dropna(axis=1)
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_data)

# Bước 3: Sử dụng Elbow Method để tìm số cụm tối ưu
distortions = []
K = range(1, 11)  # Thử nghiệm từ 1 đến 10 cụm

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    # Tính tổng khoảng cách của các điểm trong cụm tới tâm cụm
    distortions.append(sum(np.min(cdist(scaled_data, kmeans.cluster_centers_, 'euclidean'), axis=1)) / scaled_data.shape[0])

# Vẽ biểu đồ Elbow
plt.figure(figsize=(8, 5))
plt.plot(K, distortions, 'bo-')
plt.xlabel('Số cụm K')
plt.ylabel('Distortion')
plt.title('Elbow Method để tìm số cụm tối ưu')
plt.show()

# Bước 4: Áp dụng K-means 
optimal_k = 3  # Thay giá trị này sau khi quan sát biểu đồ Elbow
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
data['Cluster'] = kmeans.fit_predict(scaled_data)

# Giảm chiều dữ liệu xuống 2 chiều
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

# Thêm các cột PCA vào DataFrame
data['PCA1'] = pca_data[:, 0]
data['PCA2'] = pca_data[:, 1]

# Vẽ biểu đồ phân cụm trên mặt phẳng 2D
plt.figure(figsize=(10, 7))
sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster', data=data, palette='viridis', s=100, alpha=0.7)
plt.title('Phân cụm cầu thủ trên mặt phẳng 2D sau khi giảm chiều bằng PCA')
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.legend(title='Cụm')
plt.show()
