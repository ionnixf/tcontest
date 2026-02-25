import sys
from collections import defaultdict


def normalize(word):
    return ''.join(c for c in word.lower() if c.isalpha() or c == "'")


def differ_by_one(w1, w2):
    diff = 0
    for a, b in zip(w1, w2):
        if a != b:
            diff += 1
            if diff > 1:
                return False
    return diff == 1


def build_graph(uw):
    g = defaultdict(set)

    wc = [w for w in uw if len(w) > 1]

    byl = defaultdict(list)
    for w in wc:
        byl[len(w)].append(w)

    for ln, ws in byl.items():
        n = len(ws)
        for i in range(n):
            for j in range(i + 1, n):
                if differ_by_one(ws[i], ws[j]):
                    g[ws[i]].add(ws[j])
                    g[ws[j]].add(ws[i])

    lengths = sorted(byl.keys())
    for ln in lengths:
        if ln - 1 in byl:
            for shorter in byl[ln - 1]:
                for longer in byl[ln]:
                    if longer[:-1] == shorter and longer[-1] in 'es':
                        g[shorter].add(longer)
                        g[longer].add(shorter)

    return g


def find_components(uw, g):
    vis = set()
    comps = []

    for w in uw:
        if w not in vis:
            comp = []
            q = [w]
            vis.add(w)
            while q:
                cur = q.pop(0)
                comp.append(cur)
                for nb in g[cur]:
                    if nb not in vis:
                        vis.add(nb)
                        q.append(nb)
            comps.append(comp)

    return comps


def count_contextual_freq(ws, w2r, k):
    n = len(ws)
    r2f = defaultdict(int)

    for i in range(n):
        w = ws[i]
        r = w2r[w]

        s = max(0, i - k)
        e = min(n, i + k + 1)

        has = False
        for j in range(s, e):
            if j != i and w2r[ws[j]] == r:
                has = True
                break

        if has:
            r2f[r] += 1

    return r2f


def main():
    lines = sys.stdin.read().split('\n')

#    if not lines:
#        return

    k = int(lines[0].strip())

    ws = []
    for line in lines[1:]:
        if not line.strip():
            break
        for w in line.split():
            norm = normalize(w)
            if norm:
                ws.append(norm)

    uw = list(set(ws))

    g = build_graph(uw)

    comps = find_components(uw, g)

    w2r = {}
    for comp in comps:
        rep = min(comp)
        for w in comp:
            w2r[w] = rep

    r2f = count_contextual_freq(ws, w2r, k)

    res = [(r, f) for r, f in r2f.items() if f > 0]
    res.sort(key=lambda x: (-x[1], x[0]))

    for r, f in res:
        print(f"{r}: {f}")


if __name__ == "__main__":
    main()