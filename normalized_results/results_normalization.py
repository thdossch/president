from matplotlib import pyplot as plt
plt.plot([1, 2, 3, 4]
, [43.19, 37.91, 39.01, 40.67], 'r', label='normal')
plt.plot([1, 2, 3, 4]
, [28.4, 25.46, 38.28, 40.09], 'b', label='normalized')

plt.xlabel("Network")
plt.ylabel("W/L in %")
axes = plt.gca()
axes.set_ylim([0, 100])
plt.legend(loc="upper right")
plt.xticks([1, 2, 3, 4])
plt.show()


