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
        shortest_path_list = []
        if u in self.labels[best_landmark][0] and v in self.labels[best_landmark][0]:
            path_length = self.labels[best_landmark][0][u] + self.labels[best_landmark][0][v]
            path_to_landmark = self.get_path(best_landmark, u)[:-1]
            path_from_landmark = self.get_path(best_landmark, v)[::-1]
            path = path_to_landmark + path_from_landmark
            if path_length < shortest_path_length:
                shortest_path_length = path_length
                shortest_path_list = [path] 
        return shortest_path_length, shortest_path_list

    def get_path(self, landmark, v):
        path = []
        while v is not None:
            path.append(v)
            v = self.labels[landmark][1].get(v)
        return path

    def update_bandwidth(self, path, flow_size):
        for i in range(len(path) - 1):
            self.graph_dict[path[i]][path[i+1]]['bandwidth'] -= flow_size


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


    def get_path_total_utilization(self, path):
        total_utilization = 0
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            utilization = 1 - self.graph_dict[u][v]['bandwidth'] / self.graph_dict[u][v]['initial_bandwidth']
            total_utilization += utilization
        return total_utilization

    def get_best_landmark_set(self, landmarks, src, dest, bw, C):
        best_landmarks = []
        available_landmarks = landmarks.copy()  # 创建一个可用地标的副本

        for _ in range(C):
            min_score = float('inf')
            best_landmark = None
            best_path = None

            # 使用一个临时的图来保存当前的状态
            temp_graph_dict = copy.deepcopy(self.graph_dict)
            temp_labels = copy.deepcopy(self.labels)

            for landmark in available_landmarks:
                # Construct the index with the current landmark.
                self.construct_index([landmark])
                _, paths = self.query(src, dest, landmark)
                for path in paths:
                    # Calculate the score for the current path
                    total_utilization = self.get_path_total_utilization(path)
                    score = total_utilization

                    if score < min_score:
                        min_score = score
                        best_landmark = landmark
                        best_path = path

            # If we found a best landmark and path, update the bandwidth on the temporary graph
            if best_landmark and best_path:
                self.construct_index([best_landmark])
                self.update_bandwidth([best_path], bw/C)
                best_landmarks.append(best_landmark)
                available_landmarks.remove(best_landmark)  # Remove the selected landmark from the available list

                # Update the main graph_dict and labels to the current state after bandwidth update
                self.graph_dict = copy.deepcopy(temp_graph_dict)
                self.labels = copy.deepcopy(temp_labels)
                self.update_bandwidth([best_path], bw/C)
            else:
                break  # If no best landmark is found, break out of the loop

        return best_landmarks




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
    K = 10  
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

    C = 2  # Define the number of landmarks you want to use
    for src, dest, bw in D:
        # Construct the index with the best landmark set.
        best_landmarks = pll.get_best_landmark_set(k_landmarks, src, dest, bw, C)
        print('best_landmarks=', best_landmarks, 'bw=', bw/C)
        
        for landmark in best_landmarks:
            pll.construct_index([landmark])
            length, paths = pll.query(src, dest, landmark)
            print(f'Shortest path length from {src} to {dest} using {landmark}:', length)
            for path in paths:
                print(f'Shortest path from {src} to {dest} using {landmark}:', path)
            # Update bandwidth for the path
            pll.update_bandwidth(path, bw/C)
            all_paths.extend(paths)  # 将路径添加到all_paths列表中

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

