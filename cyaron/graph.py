import random

class Edge:
    def __init__(self, u, v, w):
        self.start = u
        self.end = v
        self.weight = w

    def __str__(self):
        return "%d %d %d" % (self.start, self.end, self.weight)

class Graph:
    def __init__(self, point_count, directed=False):
        self.directed = directed
        self.edges = [[] for i in range(point_count+1)]

    def to_str(self, **kwargs):
        shuffle = kwargs.get("shuffle",False)
        op = kwargs.get("output",str)
        buf = []
        if shuffle:
            tmp = [i for i in range(1,len(self.edges))]
            random.shuffle(tmp)
            tmp = [0] + tmp
            tat = []
            for edge in self.iterate_edges():
                tat.append(Edge(tmp[edge.start], tmp[edge.end], edge.weight))
            random.shuffle(tat)
            for edge in tat:
                if not self.directed and random.randint(0,1) == 0:
                    (edge.start, edge.end)=(edge.end, edge.start)
                buf.append(op(edge))
        else:
            for edge in self.iterate_edges():
                buf.append(op(edge))
        return "\n".join(buf)

    def __str__(self):
        return self.to_str()

    def iterate_edges(self):
        for node in self.edges:
            for edge in node:
                if edge.end >= edge.start or self.directed:
                    yield edge

    def __add_edge(self, x, y, w):
        self.edges[x].append(Edge(x, y, w))

    def add_edge(self, x, y, **kwargs):
        weight = kwargs.get("weight", 1)
        self.__add_edge(x, y, weight)
        if not self.directed and x != y:
            self.__add_edge(y, x, weight)

    @staticmethod
    def chain(point_count, **kwargs):
        return Graph.tree(point_count, 1, 0, **kwargs)

    @staticmethod
    def flower(point_count, **kwargs):
        return Graph.tree(point_count, 0, 1, **kwargs)

    @staticmethod
    def tree(point_count, chain=0, flower=0, **kwargs):
        directed = kwargs.get("directed", False)
        weight_limit = kwargs.get("weight_limit", (1, 1))
        if not isinstance(weight_limit, tuple):
            weight_limit = (1, weight_limit)

        if not 0 <= chain <= 1 or not 0 <= flower <= 1:
            raise Exception("chain and flower must be between 0 and 1")
        if chain+flower > 1:
            raise Exception("chain plus flower must be smaller than 1")

        graph = Graph(point_count, directed)
        chain_count = int((point_count-1) * chain)
        flower_count = int((point_count-1) * flower)
        if chain_count > point_count - 1:
            chain_count = point_count - 1
        if chain_count + flower_count > point_count - 1:
            flower_count = point_count - 1 - chain_count
        random_count = point_count - 1 - chain_count - flower_count

        for i in range(2, chain_count+2):
            weight = random.randint(weight_limit[0], weight_limit[1])
            graph.add_edge(i-1, i, weight=weight)

        for i in range(chain_count+2, chain_count+flower_count+2):
            weight = random.randint(weight_limit[0], weight_limit[1])
            graph.add_edge(1, i, weight=weight)

        for i in range(point_count-random_count+1, point_count+1):
            weight = random.randint(weight_limit[0], weight_limit[1])
            u = random.randrange(1, i)
            graph.add_edge(u, i, weight=weight)

        return graph

    @staticmethod
    def binary_tree(point_count, left=0, right=0, **kwargs):
        directed = kwargs.get("directed", False)
        weight_limit = kwargs.get("weight_limit", (1, 1))
        if not isinstance(weight_limit, tuple):
            weight_limit = (1, weight_limit)

        if not 0 <= left <= 1 or not 0 <= right <= 1:
            raise Exception("left and right must be between 0 and 1")
        if left+right > 1:
            raise Exception("left plus right must be smaller than 1")

        can_left = {1}
        can_right = {1}
        graph = Graph(point_count,directed)
        for i in range(2, point_count+1):
            edge_pos = random.uniform(0, 1)
            weight = random.randint(weight_limit[0], weight_limit[1])

            node = 0
            if edge_pos < left or left+right < edge_pos <= (1.0-left-right)/2: # Left
                node = random.choice(tuple(can_left))
                can_left.remove(node)
            elif left <= edge_pos <= left+right or (1.0-left-right)/2 < edge_pos < 1: # Right
                node = random.choice(tuple(can_right))
                can_right.remove(node)

            graph.add_edge(node, i, weight=weight)
            can_left.add(i)
            can_right.add(i)

        return graph

    @staticmethod
    def graph(point_count, edge_count, **kwargs):
        directed = kwargs.get("directed", False)
        weight_limit = kwargs.get("weight_limit", (1,1))
        if not isinstance(weight_limit, tuple):
            weight_limit = (1, weight_limit)
        graph = Graph(point_count,directed)
        for i in range(edge_count):
            u = random.randint(1, point_count)
            v = random.randint(1, point_count)
            weight = random.randint(weight_limit[0], weight_limit[1])
            graph.add_edge(u, v, weight=weight)
        return graph

    #hack spfa (maybe?)
    @staticmethod
    def hack_spfa(point_count, **kwargs):
        directed = kwargs.get("directed", False)
        extraedg = kwargs.get("extra_edge", 2)
        weight_limit = kwargs.get("weight_limit", (1,1))
        if not isinstance(weight_limit, tuple):
            weight_limit = (1, weight_limit)
        skp=point_count+3
        graph=Graph(point_count,directed)
        if point_count%2==1:
            skp=point_count/2+1
        half=point_count/2
        for i in range(1,half):
            (x,y)=(i,i+1)
            weight = random.randint(weight_limit[0], weight_limit[1])
            graph.add_edge(x+(x>=skp),y+(y>=skp),weight=weight)
            (x,y)=(i+half,i+half+1)
            weight = random.randint(weight_limit[0], weight_limit[1])
            graph.add_edge(x+(x>=skp),y+(y>=skp),weight=weight)
        for i in range(1,half+1):
            (x,y)=(i,i+half)
            weight = random.randint(weight_limit[0], weight_limit[1])
            graph.add_edge(x+(x>=skp),y+(y>=skp),weight=weight)
        for i in range(extraedg):
            u = random.randint(1, point_count)
            v = random.randint(1, point_count)
            weight = random.randint(weight_limit[0], weight_limit[1])
            graph.add_edge(u, v, weight=weight)
        return graph
