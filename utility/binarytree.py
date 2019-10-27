class Tree:
    def __init__(self, value, left=None, right=None):
        if left is not None:
            if not isinstance(left, Tree):
                raise TypeError("Left subtree is not a class tree")
        if left is not None:
            if not isinstance(right, Tree):
                raise TypeError("Right subtree is not a class tree")
        self.value = value
        self.left = left
        self.right = right

    def __iter__(self):
        cur_vertex = [self]
        while len(cur_vertex) > 0:
            next_vertex = []
            for vertex in cur_vertex:
                yield vertex
                if vertex.left is not None:
                    next_vertex.append(vertex.left)
                if vertex.right is not None:
                    next_vertex.append(vertex.right)
            cur_vertex = next_vertex

    def __len__(self):
        length = 1
        cur_vertex = [self]
        while len(cur_vertex) > 0:
            next_vertex = []
            for vertex in cur_vertex:
                if vertex.left is not None:
                    next_vertex.append(vertex.left)
                    length += 1
                if vertex.right is not None:
                    next_vertex.append(vertex.right)
                    length += 1
            cur_vertex = next_vertex

    @property
    def height(self):
        height = 0
        cur_vertex = [self]
        while len(cur_vertex) > 0:
            next_vertex = []
            height += 1
            for vertex in cur_vertex:
                if vertex.left is not None:
                    next_vertex.append(vertex.left)
                if vertex.right is not None:
                    next_vertex.append(vertex.right)
            cur_vertex = next_vertex

        return height
