m = 10000 # max value
result = dist = [
	[0, 1, 4],
	[m, 0, 2],
	[2, m, 0]]
nodes = len(dist)
indexes = range(nodes)
for k in indexes:
    distk = dist[k]
    for i in indexes:
        if i == k: continue
        disti = dist[i]
        for j in indexes:
            if j == i or j == k: continue
            ikj = disti[k] + distk[j]
            if disti[j] > ikj:
                disti[j] = ikj
print(result[0][2])