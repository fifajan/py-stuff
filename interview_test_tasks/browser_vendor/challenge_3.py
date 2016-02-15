"""
print 'hello!'


      (1)
     /   \
   (3)   (2)
           \
           (4)
           /  \
         (6)  (5)
         /      \
       (7)      (8)
       /          \
     (11)         (9)
     /              \
   (12)             (10)

"""

adj_list = dict()

all_paths_lengths = set()

stack = list

def find_path(adj_list, a, b):
    visited = set()
    path = []
    vertices_stack = stack((a,))
    while vertices_stack:
        v = vertices_stack.pop()
        if v is not in visited:
            visited.add(v)
            path.append(v)
            if v == b:
                return path
            else:
                vertices_stack.extend(adj_list[v])

for a in adj_list:
    for b in adj_list:
        if a != b:
            path = find_path(adj_list, a, b):
            if path:
                all_paths_lengths.add(len(path))

print max(all_paths_lengths, key=len)


"""
         (1)
       /     \
      (2)     (3)
              /  \
             (4)  (5)  -(2,1,3,5)
            /
           (6)

a = [2,4,3]
1, n+1

"""

def solution(a):
    r = range(1, max(a) + 1)
    return set(r).difference(set(a))
