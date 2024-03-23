import queue
import copy
import random
import networkx as nx
import matplotlib.pyplot as plt

class Dijkstra:
    def __init__(self, graph):
        self.graph = graph

    def average_hop_count(self, paths):
        total_hops = sum(len(path) - 1 for path in paths)
        return total_hops / len(paths)

    def query(self, src, dest):
        try:
            path = nx.dijkstra_path(self.graph, src, dest, weight='weight')
            length = nx.dijkstra_path_length(self.graph, src, dest, weight='weight')
            return length, path
        except nx.NetworkXNoPath:
            return float('inf'), []

    def update_bandwidth(self, path, flow_size):
        for i in range(len(path) - 1):
            self.graph[path[i]][path[i+1]]['bandwidth'] -= flow_size

    def get_max_utilization_link(self):
        max_utilization = 0
        max_link = None
        for u, v, data in self.graph.edges(data=True):
            utilization = 1 - data['bandwidth'] / data['initial_bandwidth']
            if utilization > max_utilization:
                max_utilization = utilization
                max_link = (u, v)
        return max_link, max_utilization

def main():
    # 从文件中读取图
    G = nx.read_gml("E:/project/Topology/ChinaTelecom.gml", destringizer=None)
    
    # 将所有边的权重设置为10，并设置带宽为1000
    for u, v, d in G.edges(data=True):
        d['weight'] = 10
        d['bandwidth'] = 1000
        d['initial_bandwidth'] = 1000

    # 绘制图
    plt.figure(figsize=(15, 20))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='green', edge_color='red')
    plt.show()
    
    dijkstra = Dijkstra(G)

    D = []
    nodes = list(G.nodes())  # N6到N17为边缘节点
    all_paths = []

    for _ in range(1000):
        src = random.choice(nodes)
        dest = random.choice(nodes)
        while dest == src:  # 确保目的节点和源节点不同
            dest = random.choice(nodes)
        bw = random.randint(10, 10)  # 10-20M之间的随机带宽
        D.append((src, dest, bw))

    # Simulate some flows and update the network bandwidth
    for src, dest, bw in D:
        length, path = dijkstra.query(src, dest)
        print(f'Shortest path length from {src} to {dest}:', length)
        print(f'Shortest path from {src} to {dest}:', path)
        dijkstra.update_bandwidth(path, bw)
        all_paths.append(path)  # 将路径添加到all_paths列表中

    # Query the link with the maximum utilization
    max_link, max_utilization = dijkstra.get_max_utilization_link()
    print('Link with maximum utilization:', max_link)
    print('Maximum utilization:', "{:.2%}".format(max_utilization))
 
    # 计算并打印平均跳数
    avg_hop_count = dijkstra.average_hop_count(all_paths)
    print('Average hop count:', avg_hop_count)

    #pll.get_utilization_links()

if __name__ == '__main__':
    main()

