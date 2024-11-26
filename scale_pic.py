import matplotlib.pyplot as plt

# 数据
x_labels = ["small", "medium", "large"]
data1 = [0.039, 0.018, 0.009]
data2 = [0.07, 0.098, 0.125]
data3 = [0.245, 0.128, 0.118]

# 设置字体
plt.rcParams["font.family"] = "Times New Roman"

# 创建图形和轴
fig, ax = plt.subplots()

# 绘制折线图
ax.plot(x_labels, data1, marker='o', label='Cycle Check', color='#1f77b4', linewidth=2, markersize=8)
ax.plot(x_labels, data2, marker='s', label='Path Existence', color='#ff7f0e', linewidth=2, markersize=8)
ax.plot(x_labels, data3, marker='^', label='Euler Graph', color='#2ca02c', linewidth=2, markersize=8)

# 添加标题和标签
# ax.set_title('Comparison of Data Sets', fontsize=14)
ax.set_xlabel('Graph Scale', fontsize=16)
ax.set_ylabel('D-value', fontsize=16)

# 设置坐标轴刻度字体大小
ax.tick_params(axis='both', labelsize=13)

# 显示图例并设置字体大小
ax.legend(fontsize=13)

# 优化布局
plt.tight_layout()

# 保存为 PDF
plt.savefig('./scale_pic.pdf', format='pdf')

# 显示图形
plt.show()
