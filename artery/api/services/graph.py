class Node:
    city_id: int
    index: int

    def __init__(self, city_id: int):
        self.city_id = city_id
        self.index = None

class Edge:
    properties: dict[str, float | int]

    def __init__(self, **kwargs) -> None:
        self.properties = kwargs

    def __getitem__(self, property: str) -> float | int:
        return self.properties[property]

class Path:
    def __init__(self, length, path: list) -> None:
        self.lenght = length
        self.path = path

class Graph:
    nodes: list[Node]
    adg_mat: list[dict]

    @classmethod
    def create_from_nodes(self, nodes: list[int]):
        return Graph(len(nodes), len(nodes), nodes)
  
    def __init__(self, row, col, nodes: list[int] = None):
        self.adj_mat = [[None] * col for _ in range(row)]
        self.nodes = [Node(id) for id in nodes]
        for i in range(len(self.nodes)):
            self.nodes[i].index = i

    def connect_dir(self, node1: Node, node2: Node, edge: dict):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = edge
  
    def connect(self, node1: Node, node2: Node, edge: dict):
        self.connect_dir(node1, node2, edge) 
        self.connect_dir(node2, node1, edge) 

    def connections_from(self, node: Node) -> list:
        node_index = self.get_index_from_node(node)
        return [(self.nodes[col_num], self.adj_mat[node_index][col_num]) for col_num in range(len(self.adj_mat[node_index])) if self.adj_mat[node_index][col_num] != None]

    def connections_to(self, node: Node):
        node = self.get_index_from_node(node)
        column = [row[node] for row in self.adj_mat]
        return [(self.nodes[row_num], column[row_num]) for row_num in range(len(column)) if column[row_num] != None]
     
  
    def print_adj_mat(self):
        for row in self.adj_mat:
            for i in row:
                if i == None:
                    print(i, end='\t')
                else:
                    print(type(i), end='\t')
            print()
  
    def node(self, index) -> Node:
        return self.nodes[index]
    
  
    def remove_conn(self, node1, node2):
        self.remove_conn_dir(node1, node2)
        self.remove_conn_dir(node2, node1)
   
    def remove_conn_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = None
  
    def can_traverse_dir(self, node1, node2) -> bool:
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        return self.adj_mat[node1][node2] != None
  
    def has_conn(self, node1, node2) -> bool:
        return self.can_traverse_dir(node1, node2) or self.can_traverse_dir(node2, node1)
  
    def add_node(self, node: Node):
        self.nodes.append(node)
        node.index = len(self.nodes) - 1
        for row in self.adj_mat:
            row.append(None)     
        self.adj_mat.append([None] * (len(self.adj_mat) + 1))

    def get_edge(self, n1, n2) -> dict[str, float]:
        node1, node2 = self.get_index_from_node(n1), self.get_index_from_node(n2)
        return self.adj_mat[node1][node2].properties
  
    def get_index_from_node(self, node):
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError("node must be an integer or a Node object")
        if isinstance(node, int):
            return node
        else:
            return node.index
    
    def get_node_by_id(self, id: int) -> Node:
        for node in self.nodes:
            if node.city_id == id:
                return node

    def dijkstra(self, start: Node, end: Node, property: str) -> Path:
        dist_to = { node: 0 for node in self.nodes }
        for i in dist_to:
            dist_to[i] = [float('inf'), [start.city_id]]
       
        dist_to[start][0] = 0
        queue = self.nodes[:]
        seen = set()
        while len(queue) > 0:
            min_dist = float("inf")
            min_node = None
            for n in queue: 
                print(n.city_id, '--', dist_to[n][0], end='|')
                if dist_to[n][0] < min_dist and n not in seen:
                    min_dist = dist_to[n][0]
                    min_node = n
            print()
            queue.remove(min_node)
            seen.add(min_node)
            connections = self.connections_from(min_node)
            for (node, edge) in connections: 
                tot_dist = edge[property] + min_dist
                if tot_dist < dist_to[node][0]:
                    dist_to[node][0] = tot_dist
                    dist_to[node][1] = list(dist_to[min_node][1])
                    dist_to[node][1].append(node.city_id)
        
        for key in dist_to:
            if key == end:
                return Path(dist_to[key][0], dist_to[key][1])

def test_graph():
    a = Node("A") #34
    b = Node("B") #33
    c = Node("C") #32
    d = Node("D") #31
    e = Node("E") #30
    f = Node("F") #29
    
    w_graph = Graph.create_from_nodes([a,b,c,d,e,f])
    
    w_graph.connect(a,b, Edge(weight=5, time=10, cost=6))
    w_graph.connect(a,c, Edge(weight=10, time=10, cost=6))
    w_graph.connect(a,e, Edge(weight=2, time=10, cost=6))
    w_graph.connect(b,c, Edge(weight=2, time=10, cost=6))
    w_graph.connect(b,d, Edge(weight=4, time=10, cost=6))
    w_graph.connect(c,d, Edge(weight=7, time=10, cost=6))
    w_graph.connect(c,f, Edge(weight=10, time=10, cost=6))
    w_graph.connect(d,e, Edge(weight=3, time=10, cost=6))

    print('by weight')
    path = w_graph.dijkstra(a, f, 'weight')
    for n in path.path:
        print(n.data)

def test_graph():
    a = Node('a') #34
    b = Node('b') #33
    c = Node('c') #32
    d = Node('d') #31
    e = Node('e') #30
    f = Node('f') #29
    
    cities = [34, 33, 32, 31, 30, 29]
    roads = [
        { 'road_id': 1, 'city_start_id': 34, 'city_end_id': 33, 'lenght': 5, 'time': 10, 'cost': 6 },
        { 'road_id': 2, 'city_start_id': 34, 'city_end_id': 32, 'lenght': 10, 'time': 10, 'cost': 6 },
        { 'road_id': 3, 'city_start_id': 34, 'city_end_id': 30, 'lenght': 2, 'time': 10, 'cost': 6 },
    
        { 'road_id': 4, 'city_start_id': 33, 'city_end_id': 32, 'lenght': 2, 'time': 10, 'cost': 6 },
        { 'road_id': 5, 'city_start_id': 33, 'city_end_id': 31, 'lenght': 4, 'time': 10, 'cost': 6 },
    
        { 'road_id': 6, 'city_start_id': 32, 'city_end_id': 31, 'lenght': 7, 'time': 10, 'cost': 6 },
        { 'road_id': 7, 'city_start_id': 32, 'city_end_id': 29, 'lenght': 10, 'time': 10, 'cost': 6 },
    
        { 'road_id': 8, 'city_start_id': 31, 'city_end_id': 30, 'lenght': 3, 'time': 10, 'cost': 6 },
    ]
    
    paths = make_route(cities, roads, [34], 29, 'lenght')
    for path in paths:
        print(path.lenght, path.path)
   

        
def make_route(cities: list[int], roads: list[dict], stock_cities: list[int], client_city: int, by: str) -> list[list[int]]:
    map = Graph.create_from_nodes(cities)
    for road in roads:
        node1, node2 = map.get_node_by_id(road['city_start_id']), map.get_node_by_id(road['city_end_id'])
        map.connect(node1, node2, road)

    paths = []
    end = map.get_node_by_id(client_city)
    for stock_id in stock_cities:
        start = map.get_node_by_id(stock_id)
        path = map.dijkstra(start, end, by)
        paths.append(path)

    return paths 

