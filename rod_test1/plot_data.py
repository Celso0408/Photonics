import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

te_freqs = pd.read_csv ('tri-rods.te.dat')
tm_freqs = pd.read_csv ('tri-rods.te.dat')

# te_freqs = np.array(te_freqs)
# tm_freqs = np.array(tm_freqs)

fig, ax = plt.subplots()
x = range(len(tm_freqs))

# Plot bands
# Scatter plot for multiple y values, see https://stackoverflow.com/a/34280815/2261298
# for xz, tmz, tez in zip(x, tm_freqs, te_freqs):
#     ax.scatter([xz]*len(tmz), tmz, color='blue')
#     ax.scatter([xz]*len(tez), tez, color='red', facecolors='none')
ax.plot(tm_freqs[1], color='blue')
ax.plot(te_freqs[1], color='red')
ax.set_ylim([0, 1])
ax.set_xlim([x[0], x[-1]])
# 
# # Plot gaps
# for gap in tm_gaps:
#     if gap[0] > 1:
#         ax.fill_between(x, gap[1], gap[2], color='blue', alpha=0.2)
# # 
# for gap in te_gaps:
#     if gap[0] > 1:
#         ax.fill_between(x, gap[1], gap[2], color='red', alpha=0.2)
# # 
# # 
# # Plot labels
# ax.text(12, 0.04, 'TM bands', color='blue', size=15)
# ax.text(13.05, 0.235, 'TE bands', color='red', size=15)
# 
# points_in_between = (len(tm_freqs) - 4) / 3
# tick_locs = [i*points_in_between+i for i in range(4)]
# tick_labs = ['Γ', 'X', 'M', 'Γ']
# ax.set_xticks(tick_locs)
# ax.set_xticklabels(tick_labs, size=16)
# ax.set_ylabel('frequency (c/a)', size=16)
# ax.grid(True)
# 
plt.show()
