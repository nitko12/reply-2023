from pprint import pprint
import gurobipy as gp
from gurobipy import GRB


def main():
    m, n, k = map(int, input().split())

    lens = list(map(int, input().split()))

    a = [
        input().split()
        for _ in range(n)
    ]

    model = gp.Model("zzt")

    x = model.addVars(
        n,
        m,
        vtype=GRB.BINARY,
        name="x"
    )

    start_ends = model.addVars(
        n,
        m,
        vtype=GRB.BINARY,
        name="x"
    )

    for i in range(n):
        for j in range(m):
            if a[i][j] == '*':
                model.addConstr(x[i, j] == 0)

    for i in range(n):
        for j in range(m):
            dx = [-1, 0, 0, 1]
            dy = [0, -1, 1, 0]

            neighbors = []

            for d in range(4):
                xx = (j + dx[d]) % m
                yy = (i + dy[d]) % n

                neighbors.append(x[yy, xx])

            model.addConstr(
                (x[i, j] == 1) >> (gp.quicksum(neighbors) >= 2 - start_ends[i, j])
            )

    model.addConstr(gp.quicksum(start_ends) == 2)

    model.addConstr(gp.quicksum(x) == lens[0])

    obj = gp.LinExpr()

    for i in range(n):
        for j in range(m):
            if a[i][j] != '*':
                obj += int(a[i][j]) * x[i, j]

    model.setObjective(obj, GRB.MAXIMIZE)

    model.optimize()

    for i in range(n):
        for j in range(m):
            print(1 if x[i, j].x > 0.5 else 0, end=' ')

        print()

    print()

    for i in range(n):
        for j in range(m):
            print(1 if start_ends[i, j].x > 0.5 else 0, end=' ')

        print()

    print()

    for i in range(n):
        for j in range(m):
            dx = [-1, 0, 0, 1]
            dy = [0, -1, 1, 0]

            neighbors = []

            for d in range(4):
                xx = (j + dx[d]) % m
                yy = (i + dy[d]) % n

                neighbors.append(x[yy, xx])

            neighbors_x = [xx.x for xx in neighbors]

            print(int(sum(neighbors_x)), end=' ')

        print()


if __name__ == "__main__":
    main()
