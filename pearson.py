import numpy as np

def pearson_correlation(x, y):
    # Tính giá trị trung bình
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    # Tính độ lệch chuẩn
    std_x = np.std(x)
    std_y = np.std(y)
    
    # Tính hệ số tương quan Pearson
    correlation = np.sum((x - mean_x) * (y - mean_y)) / (len(x) * std_x * std_y)
    
    return correlation

# Ví dụ:
x = np.array([1, 2, 3, 4, 5, 1, 2])
y = np.array([2, 3, 4, 5, 6, 8, 10])

print("Hệ số tương quan Pearson:", pearson_correlation(x, y))
