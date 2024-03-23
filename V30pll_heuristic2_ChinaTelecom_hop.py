import queue
import copy
import random
import networkx as nx
import matplotlib.pyplot as plt

class PrunedLandmarkLabeling:
    def __init__(self, graph, graph_dict):
        self.graph = graph
        self.graph_dict = graph_dict
        self.labels = {}

    def average_hop_count(self, paths):
        total_hops = sum(len(path) - 1 for path in paths)
        return total_hops / len(paths)
    
    def construct_index(self, landmarks):
        for v in landmarks:
            self.labels[v] = self.pruned_bfs(v)

    def pruned_bfs(self, start):
        dist = {v: float('inf') for v in self.graph_dict}
        prev = {v: None for v in self.graph_dict}
        dist[start] = 0
        q = queue.PriorityQueue()
        q.put((0, start))
        while not q.empty():
            _, v = q.get()
            for w, data in self.graph_dict[v].items():
                weight = data['weight']
                alt = dist[v] + weight
                if alt < dist[w]:
                    dist[w] = alt
                    prev[w] = v
                    q.put((alt, w))
        return dist, prev

    def query(self, u, v, best_landmark):
        shortest_path_length = float('inf')
        shortest_path = []
        if u in self.labels[best_landmark][0] and v in self.labels[best_landmark][0]:
            path_length = self.labels[best_landmark][0][u] + self.labels[best_landmark][0][v]
            path_to_landmark = self.get_path(best_landmark, u)[:-1]
            path_from_landmark = self.get_path(best_landmark, v)[::-1]
            path = path_to_landmark + path_from_landmark
            if path_length < shortest_path_length:
                shortest_path_length = path_length
                shortest_path = path
        return shortest_path_length, shortest_path

    def get_path(self, landmark, v):
        path = []
        while v is not None:
            path.append(v)
            v = self.labels[landmark][1].get(v)
        return path

    def update_bandwidth(self, path, flow_size):
        for i in range(len(path) - 1):
            self.graph_dict[path[i]][path[i+1]]['bandwidth'] -= flow_size
            #self.graph_dict[path[i+1]][path[i]]['bandwidth'] -= flow_size

    def get_max_utilization_link(self):
        max_utilization = 0
        max_link = None
        for u, neighbors in self.graph_dict.items():
            for v, data in neighbors.items():
                utilization = 1 - data['bandwidth'] / data['initial_bandwidth']
                if utilization > max_utilization:
                    max_utilization = utilization
                    max_link = (u, v)
        return max_link, max_utilization
    
    def get_utilization_links(self):
        for u, neighbors in self.graph_dict.items():
            for v, data in neighbors.items():
                utilization = 1 - data['bandwidth'] / data['initial_bandwidth']
                if utilization > 0:
                    print(f'Link: {u, v}, Utilization: {utilization}')


    def get_path_max_utilization(self, path):
        max_utilization = 0
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            utilization = 1 - self.graph_dict[u][v]['bandwidth'] / self.graph_dict[u][v]['initial_bandwidth']
            max_utilization = max(max_utilization, utilization)
        return max_utilization

    def get_best_landmark(self, landmarks, src, dest, bw):
        best_landmark = None
        min_score = float('inf')  # 初始化一个非常大的值

        for landmark in landmarks:
            # Save the current graph_dict and labels
            current_graph_dict = copy.deepcopy(self.graph_dict)
            current_labels = copy.deepcopy(self.labels)

            # Construct the index with the current landmark.
            self.construct_index([landmark])
            length, path = self.query(src, dest, landmark)
            self.update_bandwidth(path, bw)

            # Calculate the score for the current path
            max_utilization = self.get_path_max_utilization(path)
            score = max_utilization * len(path)

            # If the score is lower than the current minimum, update the best landmark
            if score < min_score:
                best_landmark = landmark
                min_score = score

            # Restore the current graph_dict and labels
            self.graph_dict = current_graph_dict
            self.labels = current_labels

        return best_landmark

    def get_random_landmark(self, landmarks):
        return random.choice(landmarks)


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

    # GSP中心性值排序
    # 初始化最佳组和最高的Group Betweenness Centrality
    top_gsp_betweenness = []
    highest_group_betweenness = 0

    # 贪婪地选择K个节点
    K = 12  
    for _ in range(K):
        best_node = None
        for node in G.nodes():
            if node in top_gsp_betweenness:
                continue 
            group = top_gsp_betweenness + [node]
            group_betweenness = nx.group_betweenness_centrality(G, group)
            if group_betweenness > highest_group_betweenness:
                best_node = node
                highest_group_betweenness = group_betweenness
        if best_node is not None:
            top_gsp_betweenness.append(best_node)
        else:
            break

    # 选择前K个节点作为地标 
    k_landmarks = top_gsp_betweenness[:K]
    print("Top K nodes by centrality:", k_landmarks)
    
    # Convert the graph to a adjacency dictionary.
    graph_dict = nx.to_dict_of_dicts(G)

    # 实例化PLL类
    pll = PrunedLandmarkLabeling(G, graph_dict)

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

    for src, dest, bw in D:
        # Construct the index with the best landmark.
        best_landmark = pll.get_best_landmark(k_landmarks, src, dest, bw)
        #best_landmark = pll.get_random_landmark(k_landmarks)
        print('best_landmark=', best_landmark, 'bw=', bw)
        pll.construct_index([best_landmark])
        length, path = pll.query(src, dest, best_landmark)
        print(f'Shortest path length from {src} to {dest}:', length)
        print(f'Shortest path from {src} to {dest}:', path)
        pll.update_bandwidth(path, bw)
        all_paths.append(path)  # 将路径添加到all_paths列表中

    # Query the link with the maximum utilization
    max_link, max_utilization = pll.get_max_utilization_link()
    print('Link with maximum utilization:', max_link)
    print('Maximum utilization:', "{:.2%}".format(max_utilization))

    # 计算并打印平均跳数
    avg_hop_count = pll.average_hop_count(all_paths)
    print('Average hop count:', avg_hop_count)

    #pll.get_utilization_links()

if __name__ == '__main__':
    main()

