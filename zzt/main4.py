from collections import defaultdict
from pprint import pprint
import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import walker


def main():
    m, n, k = map(int, input().split())

    lens = list(map(int, input().split()))

    a = [
        input().split()
        for _ in range(n)
    ]

    sol = [
        [0] * m
        for _ in range(n)
    ]

    G = nx.DiGraph()

    chars = {}

    for i in range(n):
        for j in range(m):
            if a[i][j] != '*':
                if int(a[i][j]):
                    G.add_node((i, j))

    threshold = 10

    # plot dist od a

    # plt.hist(
    #     costs,
    #     bins=100
    # )

    # plt.show()

    # exit(0)

    for i in range(n):
        for j in range(m):
            if a[i][j] != '*':
                dx = [-1, 0, 0, 1]
                dy = [0, -1, 1, 0]
                dc = "LUDR"

                for d in range(4):
                    xx = (j + dx[d]) % m
                    yy = (i + dy[d]) % n

                    if a[yy][xx] != '*':

                        if int(a[yy][xx]) < threshold:
                            continue

                        G.add_edge((i, j), (yy, xx))
                        G.add_edge((yy, xx), (i, j))

                        chars[(i, j), (yy, xx)] = dc[d]

                        # print((i, j), (yy, xx), dc[d])

    random_walks = [[] for _ in lens]

    for i, len_ in tqdm(enumerate(lens), total=len(lens)):

        X = walker.random_walks(G, n_walks=50, walk_len=len_)

        for path in X:
            print(path)
            cost, path_exp, dudl = 0, [], []

            # print(list(path))

            for k in range(len(path) - 1):
                cost += int(a[path[k][0]][path[k][1]])
            for k in range(len(path) - 1):
                path_exp.append(tuple(path[k]))
                dudl.append(chars[tuple(path[k]), tuple(path[k + 1])])

            random_walks[i].append(
                (cost, path_exp, dudl)
            )

            # print(cost, path_exp, dudl, len_)

        # print(do_random_walk(G, len_, a))

    model = gp.Model("mip1")

    x = model.addVars(
        len(random_walks),
        len(random_walks[0]),
        vtype=GRB.BINARY,
        name="x"
    )

    used = gp.tupledict(
        {
            node: gp.LinExpr(0)
            for node in G.nodes
        }
    )

    obj = gp.LinExpr(0)

    for i, len_ in enumerate(lens):
        for j, (cost, path, dudl) in enumerate(random_walks[i]):
            for node in path:
                used[node] += x[i, j]

            obj += x[i, j] * cost

    for i, len_ in enumerate(lens):
        # only one used

        model.addConstr(
            gp.quicksum(x[i, j] for j in range(len(random_walks[i]))) == 1
        )

    for node in G.nodes:
        model.addConstr(used[node] <= 1)

    model.setObjective(obj, GRB.MAXIMIZE)
    model.optimize()

    for i, len_ in enumerate(lens):
        for j, (cost, path, dudl) in enumerate(random_walks[i]):
            if x[i, j].x > 0.5:
                print(path[0][1], path[0][0], " ".join(dudl))

                # for node in path:
                #     print(node[1], node[0])
                break


if __name__ == "__main__":
    main()
