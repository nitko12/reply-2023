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

    for i in range(n):
        for j in range(m):
            if a[i][j] != '*':
                G.add_node((i, j))

    for i in range(n):
        for j in range(m):
            if a[i][j] != '*':
                dx = [-1, 0, 0, 1]
                dy = [0, -1, 1, 0]

                for d in range(4):
                    xx = (j + dx[d]) % m
                    yy = (i + dy[d]) % n

                    if a[yy][xx] != '*':
                        G.add_edge((i, j), (yy, xx))
                        G.add_edge((yy, xx), (i, j))

    for len_ in lens:

        model = gp.Model("zzt")

        print(len_, "aaaa")

        x = model.addVars(
            G.edges,
            vtype=GRB.BINARY,
            name="x"
        )

        eqs = gp.tupledict(
            {
                node: gp.LinExpr(0)
                for node in G.nodes
            })

        spawns = model.addVars(
            G.nodes,
            vtype=GRB.BINARY,
            name="spawns"
        )

        ends = model.addVars(
            G.nodes,
            vtype=GRB.BINARY,
            name="ends"
        )

        for node in G.nodes:
            model.addConstr(
                x.sum(node, '*') <= 1
            )

            model.addConstr(
                x.sum('*', node) <= 1
            )

            model.addConstr(
                (spawns[node] == 0) >> (x.sum(node, '*') == x.sum('*', node))
            )

            model.addConstr(
                (ends[node] == 0) >> (x.sum(node, '*') == x.sum('*', node))
            )

            # model.addConstr(
            #     (spawns[node] == 1) >> (
            #         x.sum(node, "*") == 1)
            # )

            # model.addConstr(
            #     (ends[node] == 1) >> (x.sum(node, '*') + 1 == x.sum('*', node))
            # )

        model.addConstr(gp.quicksum(spawns) == 1)
        model.addConstr(gp.quicksum(ends) == 1)

        for node in G.nodes:
            eqs[node] += spawns[node]
            eqs[node] -= ends[node]

            model.addConstr(
                spawns[node] + ends[node] <= 1
            )

        for edge in G.edges:
            eqs[edge[0]] += x[edge]
            eqs[edge[1]] -= x[edge]

            fr, to = edge

            model.addConstr(
                x[(fr, to)] + x[(to, fr)] <= 1
            )

        model.addConstr(gp.quicksum(x) == len_)

        obj = gp.LinExpr()

        for edge in G.edges:
            obj += x[edge] * a[edge[0][0]][edge[0][1]]

        for node in G.nodes:
            model.addConstr(eqs[node] == 0)

        model.setObjective(obj, GRB.MAXIMIZE)

        # for node in G.nodes:
        #     if sol[node[0]][node[1]] == 1:
        #         model.addConstr(spawns[node] == 0)

        for edge in G.edges:
            if sol[edge[0][0]][edge[0][1]] == 1 or sol[edge[1][0]][edge[1][1]] == 1:
                model.addConstr(x[edge] == 0)

        # add indeg and outdeg constraints

        def callback(model, where):
            if where == GRB.Callback.MIPSOL:

                G2 = nx.DiGraph()

                _x, _spawns, _ends = model._vars

                vals = model.cbGetSolution(_x)
                vals_spawn = model.cbGetSolution(_spawns)
                vals_end = model.cbGetSolution(_ends)

                to_remove = []
                for edge in G.edges:
                    if vals[edge] > 0.5:
                        G2.add_edge(edge[1], edge[0])
                        to_remove.append(_x[edge])

                spawn = [node for node in G2.nodes if vals_spawn[node] > 0.5][0]
                end = [node for node in G2.nodes if vals_end[node] > 0.5][0]

                if not nx.is_weakly_connected(G2):
                    model.cbLazy(gp.quicksum(to_remove) <= len(to_remove) - 1)

                # if not nx.has_path(G2, spawn, end):
                #     model.cbLazy(gp.quicksum(to_remove) <= len(to_remove) - 1)

        model.params.OutputFlag = 0
        model._vars = x, spawns, ends
        model.params.LazyConstraints = 1
        model.optimize(callback)

        G2 = nx.DiGraph()

        for edge in G.edges:
            if x[edge].x > 0.5:
                G2.add_edge(edge[1], edge[0])
                # G2.add_edge(edge[0], edge[1])

        start = [node for node in G.nodes if spawns[node].x > 0.5][0]
        end = [node for node in G.nodes if ends[node].x > 0.5][0]

        path = nx.shortest_path(G2, start, end)

        print(G2.edges)

        nx.draw(G2, with_labels=True)

        plt.show()

        # print UDLR

        print(start[0], start[1], end=' ')

        for i in range(1, len(path)):
            fr, to = path[i - 1], path[i]

            if fr[0] == to[0]:
                if fr[1] < to[1]:
                    print('R', end=' ')
                else:
                    print('L', end=' ')
            else:
                if fr[0] < to[0]:
                    print('D', end=' ')
                else:
                    print('U', end=' ')

        print()

        for edge in G.edges:
            if x[edge].x > 0.5:
                sol[edge[0][0]][edge[0][1]] = 1
                sol[edge[1][0]][edge[1][1]] = 1

        pprint(sol)

        # print()

        # for i in range(n):
        #     for j in range(m):
        #         if a[i][j] != '*':
        #             print(1 if spawns[i, j].x > 0.5 else 0, end=' ')
        #         else:
        #             print('* ', end='')
        #     print()

        # print()

        # for i in range(n):
        #     for j in range(m):
        #         if a[i][j] != '*':
        #             print(1 if ends[i, j].x > 0.5 else 0, end=' ')
        #         else:
        #             print('* ', end='')
        #     print()


if __name__ == "__main__":
    main()
