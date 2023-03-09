from pprint import pprint
import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import matplotlib.pyplot as plt


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
                G.add_node((i, j))

    for i in range(n):
        for j in range(m):
            if a[i][j] != '*':
                dx = [-1, 0, 0, 1]
                dy = [0, -1, 1, 0]
                dc = "ULDR"

                for d in range(4):
                    xx = (j + dx[d]) % m
                    yy = (i + dy[d]) % n

                    if a[yy][xx] != '*':
                        G.add_edge((i, j), (yy, xx))
                        chars[(i, j), (yy, xx)] = dc[d]

                        # print((i, j), (yy, xx), dc[d])

    for len_ in lens:
        model = gp.Model("zzt")

        # print(len_, "aaaa")

        x = model.addVars(
            G.edges,
            vtype=GRB.BINARY,
            name="x"
        )

        starts = model.addVars(
            G.nodes,
            vtype=GRB.BINARY,
            name="y"
        )

        ends = model.addVars(
            G.nodes,
            vtype=GRB.BINARY,
            name="z"
        )

        # add indeg = outdeg  constraint

        for node in G.nodes:
            model.addConstr(
                gp.quicksum(
                    x[edge]
                    for edge in G.in_edges(node)
                ) == gp.quicksum(
                    x[edge]
                    for edge in G.out_edges(node)
                ) - starts[node] + ends[node]
            )

            model.addConstr(
                starts[node] + ends[node] <= 1
            )

        model.addConstr(
            gp.quicksum(
                x[edge]
                for edge in G.edges
            ) == len_
        )

        for fr, to in G.edges:
            if sol[fr[0]][fr[1]] == 1:
                model.addConstr(
                    x[fr, to] == 0
                )
            if sol[to[0]][to[1]] == 1:
                model.addConstr(
                    x[fr, to] == 0
                )

        for fr, to in G.edges:
            model.addConstr(
                x[fr, to] + x[to, fr] <= 1
            )

        model.addConstr(
            starts.sum() == 1
        )

        model.addConstr(
            ends.sum() == 1
        )

        obj = gp.LinExpr(0)

        for fr, to in G.edges:
            obj += a[fr[0]][fr[1]] * x[fr, to]

        def callback(model, where):
            if where == GRB.Callback.MIPSOL:
                x, starts, ends = model._vals

                vals_x = model.cbGetSolution(x)

                G2 = nx.DiGraph()

                to_remove = []
                for edge in G.edges:
                    if vals_x[edge] > 0.5:
                        G2.add_edge(*edge)
                        to_remove.append(x[edge])

                if not nx.is_weakly_connected(G2):
                    # add lazy constraint

                    model.cbLazy(gp.quicksum(to_remove) <= len(to_remove) - 1)

                for cycle in nx.simple_cycles(G2):
                    model.cbLazy(gp.quicksum(x[fr, to] for fr, to in zip(
                        cycle, cycle[1:] + cycle[:1])) <= len(cycle) - 1)

                # exit()

        model.params.OutputFlag = 0
        model.params.LazyConstraints = 1
        model.setObjective(obj, GRB.MAXIMIZE)
        model._vals = x, starts, ends
        model.optimize(callback)

        start = [node for node in G.nodes if starts[node].x > 0.5][0]
        end = [node for node in G.nodes if ends[node].x > 0.5][0]

        # print(start, end)

        G2 = nx.DiGraph()

        for edge in G.edges:
            if x[edge].x > 0.5:
                G2.add_edge(*edge)

        nx.draw(G2, with_labels=True)

        plt.show()

        # print ULRD

        path = nx.shortest_path(G2, start, end)

        for node in path:
            sol[node[0]][node[1]] = 1

        print(start[1], start[0], end=' ')

        for fr, to in zip(path, path[1:] + path[: 1]):
            print(chars[to, fr], end='')

        print()

        # exit()


if __name__ == "__main__":
    main()
