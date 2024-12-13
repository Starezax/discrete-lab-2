"""
Lab 2 template
"""
def read_file(filename):
    """
    :param str filename: path to file
    :returns tuple[list, set] vertices and edges
    """
    with open(filename, 'r', encoding = 'utf-8') as f:
        content = f.readlines()[1:-1]
    edges = set()
    vertex = []

    for line in content:
        line = line.strip().strip(';').split(' -> ')
        edge_1, edge_2 = int(line[0]), int(line[1])
        edges.add(edge_1)
        edges.add(edge_2)
        vertex.append((edge_1, edge_2))

    return vertex, edges

def read_incidence_matrix(filename: str) -> list[list]:
    """
    :param str filename: path to file
    :returns list[list]: the incidence matrix of a given graph
    """
    edges_list, nodes_set = read_file(filename)
    nodes = sorted(nodes_set)
    node_indices = {node: idx for idx, node in enumerate(nodes)}
    incidence_matrix = [[0] * len(edges_list) for _ in range(len(nodes))]
    for edge_idx, (u, v) in enumerate(edges_list):
        u_idx = node_indices[u]
        v_idx = node_indices[v]

        incidence_matrix[u_idx][edge_idx] = -1
        incidence_matrix[v_idx][edge_idx] = 1

    return incidence_matrix

def read_adjacency_matrix(filename: str) -> list[list]:
    """
    :param str filename: path to file
    :returns list[list]: the adjacency matrix of a given graph
    """
    vertex, edges = read_file(filename)

    outp = [[0 for _ in range(len(edges))] for _ in range(len(edges))]
    for vertice in vertex:
        outp[vertice[0]][vertice[1]] = 1

    return outp

def read_adjacency_dict(filename: str) -> dict[int, list[int]]:
    """
    :param str filename: path to file
    :returns dict: the adjacency dict of a given graph
    """
    vertices, _ = read_file(filename)
    outp = {}
    for vertex in vertices:
        outp.setdefault(vertex[0], set()).add(vertex[1])
        outp.setdefault(vertex[1], set()).add(vertex[0])

    return outp


def iterative_adjacency_dict_dfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    :param list[list] graph: the adjacency list of a given graph
    :param int start: start vertex of search
    :param visited: set of visited vertices
    :returns list[int]: the dfs traversal of the graph
    >>> iterative_adjacency_dict_dfs({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
    [0, 1, 2]
    >>> iterative_adjacency_dict_dfs({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: []}, 0)
    [0, 1, 2, 3]
    """
    visited = set()
    queue = [start]
    outp = []

    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            outp.append(vertex)
            for vertex in graph[vertex]:
                if vertex not in visited:
                    queue.append(vertex)

    return outp

def iterative_adjacency_matrix_dfs(graph: list[list], start: int) ->list[int]:
    """
    :param dict graph: the adjacency matrix of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> iterative_adjacency_matrix_dfs([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0)
    [0, 1, 2]
    >>> iterative_adjacency_matrix_dfs([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]], 0)
    [0, 1, 2, 3]
    """
    visited = set()
    queue = [start]
    outp = []

    while queue:
        vertex = queue.pop()
        if vertex not in visited:
            visited.add(vertex)
            outp.append(vertex)
            for neighbor in range(len(graph[vertex]) - 1, -1, -1):
                if graph[vertex][neighbor] == 1 and neighbor not in visited:
                    queue.append(neighbor)

    return outp

def recursive_adjacency_dict_dfs(graph: dict[int, list[int]], 
start: int, outp = None, visited = None) -> list[int]:
    """
    :param list[list] graph: the adjacency list of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> recursive_adjacency_dict_dfs({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
    [0, 1, 2]
    >>> recursive_adjacency_dict_dfs({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: []}, 0)
    [0, 1, 2, 3]
    """
    if visited is None:
        visited = set()
    if outp is None:
        outp = []

    if start not in visited:
        visited.add(start)
        outp.append(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            recursive_adjacency_dict_dfs(graph, neighbor, outp, visited)

    return outp


def recursive_adjacency_matrix_dfs(graph: list[list[int]], start: int) ->list[int]:
    """
    :param dict graph: the adjacency matrix of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> recursive_adjacency_matrix_dfs([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0)
    [0, 1, 2]
    >>> recursive_adjacency_matrix_dfs([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]], 0)
    [0, 1, 2, 3]
    """
    visited = set()
    traversal = []

    def dfs(node: int):
        visited.add(node)
        traversal.append(node)
        for neighbor, connected in enumerate(graph[node]):
            if connected and neighbor not in visited:
                dfs(neighbor)

    dfs(start)
    return traversal


def iterative_adjacency_dict_bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    :param list[list] graph: the adjacency list of a given graph
    :param int start: start vertex of search
    :returns list[int]: the bfs traversal of the graph
    >>> iterative_adjacency_dict_bfs({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
    [0, 1, 2]
    >>> iterative_adjacency_dict_bfs({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: []}, 0)
    [0, 1, 2, 3]
    """
    visited = set()
    queue = [start]
    traversal = []

    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            traversal.append(vertex)
            for neighbor in sorted(graph[vertex]):
                if neighbor not in visited:
                    queue.append(neighbor)

    return traversal



def iterative_adjacency_matrix_bfs(graph: list[list[int]], start: int) ->list[int]:
    """
    :param dict graph: the adjacency matrix of a given graph
    :param int start: start vertex of search
    :returns list[int]: the bfs traversal of the graph
    >>> iterative_adjacency_matrix_bfs([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0)
    [0, 1, 2]
    >>> iterative_adjacency_matrix_bfs([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]], 0)
    [0, 1, 2, 3]
    """
    visited = set()
    queue = [start]
    traversal = []

    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            traversal.append(vertex)
            for neighbor in range(len(graph[vertex])):
                if graph[vertex][neighbor] == 1 and neighbor not in visited:
                    queue.append(neighbor)

    return traversal


def adjacency_matrix_radius(graph: list[list]) -> int:
    """
    :param list[list] graph: the adjacency matrix of a given graph
    :returns int: the radius of the graph
    >>> adjacency_matrix_radius([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    1
    """
    def bfs_matrix(start):
        n = len(graph)
        visited = [False] * n
        outp = [None] * n
        queue = [start]
        outp[start] = 0
        visited[start] = True

        while len(queue) > 0:
            curr = queue.pop(0)
            for idx, adjacent in enumerate(graph[curr]):
                if adjacent and not visited[idx]:
                    visited[idx] = True
                    outp[idx] = outp[curr] + 1
                    queue.append(idx)
        if any(dist is None for dist in outp):
            return float('inf')
        return max(outp)

    outp = [bfs_matrix(i) for i in range(len(graph))]

    return min(outp)



def adjacency_dict_radius(graph: dict[int: list[int]]) -> int:
    """
    :param dict graph: the adjacency list of a given graph
    :returns int: the radius of the graph
    >>> adjacency_dict_radius({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    1
    >>> adjacency_dict_radius({0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [1]})
    2
    """
    def bfs_dict(start):
        visited = {key: False for key in graph}
        outp = {key: None for key in graph}
        queue = [start]
        outp[start] = 0
        visited[start] = True

        while queue:
            curr = queue.pop(0)
            for el in graph[curr]:
                if not visited[el]:
                    visited[el] = True
                    outp[el] = outp[curr] + 1
                    queue.append(el)
        if any(outp[vertex] is None for vertex in graph):
            return float('inf')

        return max(outp.values())

    outp = [bfs_dict(i) for i in range(len(graph))]

    return min(outp)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
