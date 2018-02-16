import matplotlib.pyplot as plt
import numpy as np

file = open("../dictionaries/airlines_dictionary.csv")

content = file.read()
lines = content.split("\n")
counts = []
prev_val = 50000
x = []

for line in lines[2:]:
    count = line.split(",")[1]
    counts.append(count)

# Data for plotting
bins = int(len(lines) / 1000)

print(bins)

# Note that using plt.subplots below is equivalent to using
# fig = plt.figure and then ax = fig.add_subplot(111)
fig, ax = plt.subplots()
ax.plot(y=counts)

#fig.savefig("test.png")
fig.canvas.set_window_title("TEST")
plt.show()
