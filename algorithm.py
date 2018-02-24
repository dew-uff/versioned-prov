m = 10000 # max value
result = dist = [
    [0, 1, 4],
    [m, 0, 2],
    [2, m, 0],
]
nodes = len(dist)
indexes = range(nodes)
for k in indexes:
    for i in indexes:
        for j in indexes:
            ikj = dist[i][k] + dist[k][j]
            if dist[i][j] > ikj:
                dist[i][j] = ikj
print(result[0][2])