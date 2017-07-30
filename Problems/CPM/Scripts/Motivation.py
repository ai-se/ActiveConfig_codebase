content = open("BDBC_AllMeasurements.csv", "r").readlines()

performance_scores = []
for i,c in enumerate(content):
    if i == 0: continue
    performance_scores.append(float(c.split(',')[-1]))

x = range(0, len(performance_scores))
y = sorted(performance_scores)

import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot(x, y, color='red')
plt.xlabel("Number of instances (sorted based on performance scores)")
plt.ylabel("Performance Score \n(Response Time - in sec)")
plt.savefig("motivation.png")
