import heapq

def dj(g, s, t):

    dd = {x: 10**18 for x in g}  # badha nodes mate cost
    pp = {x: None for x in g}    # predecessor
    dd[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dd[u]:
            continue
        if u == t:
            break
        for v, w, _ in g[u]:
            if dd[u] + w < dd[v]:
                dd[v] = dd[u] + w
                pp[v] = u
                heapq.heappush(pq, (dd[v], v))
    if dd[t] == 10**18:
        return 10**18, []
    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        cur = pp[cur]
    path.reverse()
    return dd[t], path


def bgl(idd, poss, A, B):
    n = len(poss)
    g = {i: [] for i in range(n)}
    for u in range(n):
        for v in range(u+1, n):
            d = idd[v] - idd[u]
            ct = A * d               # direct throw cost
            if v == u+1:
                ca = 0             # adjacent passing cost 0
            else:
                ca = B * (d - 1)   # relay cost calculation, gap relay
            if ca <= ct:
                c = ca
                et = 'r'
            else:
                c = ct
                et = 't'
            g[u].append((v, c, (u, v, et)))
    return g

def pl(poss, idd, A, B):
    if not poss:
        return []
    g = bgl(idd, poss, A, B)
    _, pn = dj(g, 0, len(poss) - 1)
    return [poss[i] for i in pn]



N, M = map(int, input().split())
A, B, C = map(int, input().split())
gr = [list(input().strip()) for i in range(N)]

# aa conversion greedyly joy chhe, non-cheater ne convert karva mate jo gap cost relay karta conversion cost vadhu hoy
conv = set()
for i in range(N):
    cc = [j for j in range(M) if gr[i][j] == 'C']
    if not cc:
        continue
    for k in range(len(cc) - 1):
        s = cc[k]
        e = cc[k + 1]
        gap = e - s - 1
        if gap > 0 and B * gap > C * gap:
            for j in range(s + 1, e):
                if gr[i][j] == 'N':
                    gr[i][j] = 'C'
                    conv.add((i, j))

for j in range(M):
    rr = [i for i in range(N) if gr[i][j] == 'C']
    if not rr:
        continue
    for k in range(len(rr) - 1):
        s = rr[k]
        e = rr[k + 1]
        gap = e - s - 1
        if gap > 0 and B * gap > C * gap:
            for i in range(s + 1, e):
                if gr[i][j] == 'N':
                    gr[i][j] = 'C'
                    conv.add((i, j))

print(len(conv))
for i, j in sorted(list(conv)):
    print(i, j)

# aa rows process kare che, row-wise passing order generate kare che
for i in range(N):
    poss = []
    idxs = []
    for j in range(M):
        if gr[i][j] == 'C':
            poss.append((i, j))
            idxs.append(j)
    ordp = pl(poss, idxs, A, B)
    print(len(ordp))
    if ordp:
        print(" ".join(str(x) + " " + str(y) for x, y in ordp))
    else:
        print()

# aa columns process kare che, column-wise passing order generate kare che
for j in range(M):
    poss = []
    idxs = []
    for i in range(N):
        if gr[i][j] == 'C':
            poss.append((i, j))
            idxs.append(i)
    ordp = pl(poss, idxs, A, B)
    print(len(ordp))
    if ordp:
        print(" ".join(str(x) + " " + str(y) for x, y in ordp))
    else:
        print()
