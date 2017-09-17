"Алгоритм Дейкстры"
def dijkstra(mas):
    "Алгоритм Дейкстры"
    inf = 10 ** 10
    dist = {}
    used = {}
    path = {}
    for i in range(len(mas)):
        dist[i] = inf
        used[i] = False
        path[i] = ""
    dist[0] = 0
    min_dist = 0
    min_vertex = 0
    while min_dist < inf:
        i = min_vertex
        used[i] = True
        for item in mas[i].neighbors:
            weight = mas[i].weight_calc(mas[i].neighbors[item].neighborid)
            device_id = mas[i].neighbors[item].neighborid
            if dist[i] + weight < dist[device_id]:
                dist[device_id] = dist[i] + weight
                path[device_id] = path[i] + str(i) + " "
            min_dist = inf
        for j in range(len(mas)):
            if not used[j] and dist[j] < min_dist:
                min_dist = dist[j]
                min_vertex = j
    for i in range(len(mas)):
        print("Стоимость пути до устройства №", mas[i].deviceid, ":", dist[i], sep="")
        print("Путь до устройства №", mas[i].deviceid, ":", path[i], sep="")