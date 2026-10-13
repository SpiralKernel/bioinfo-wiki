#!/usr/bin/env python3
"""Teaching-only alignment on artificial strings; not a BLAST replacement."""
import json


def smith_waterman(query, subject, match=2, mismatch=-1, gap=-2):
    scores = [[0] * (len(subject) + 1) for _ in range(len(query) + 1)]
    trace = {}
    best = (0, 0, 0)
    for i in range(1, len(query) + 1):
        for j in range(1, len(subject) + 1):
            values = [0,
                      scores[i-1][j-1] + (match if query[i-1] == subject[j-1] else mismatch),
                      scores[i-1][j] + gap, scores[i][j-1] + gap]
            scores[i][j] = max(values)
            trace[i, j] = values.index(scores[i][j])
            if scores[i][j] > best[0]:
                best = (scores[i][j], i, j)
    score, i, j = best
    end = (i, j)
    qa, sa = [], []
    while i and j and scores[i][j] > 0:
        direction = trace[i, j]
        if direction == 1:
            qa.append(query[i-1]); sa.append(subject[j-1]); i -= 1; j -= 1
        elif direction == 2:
            qa.append(query[i-1]); sa.append('-'); i -= 1
        else:
            qa.append('-'); sa.append(subject[j-1]); j -= 1
    return {'score': score, 'query': ''.join(reversed(qa)),
            'subject': ''.join(reversed(sa)), 'start': [i, j], 'end': list(end)}


def seed_extend(query, subject, k=2, match=2, mismatch=-1, xdrop=3):
    if k < 1 or xdrop < 0:
        raise ValueError('k must be positive and xdrop nonnegative')
    index = {}
    for j in range(len(subject) - k + 1):
        index.setdefault(subject[j:j+k], []).append(j)
    hits = {}
    for i in range(len(query) - k + 1):
        for j in index.get(query[i:i+k], []):
            ends = []
            gains = []
            for qi, sj, direction in [(i-1, j-1, -1), (i+k, j+k, 1)]:
                running = best = steps = best_steps = 0
                while 0 <= qi < len(query) and 0 <= sj < len(subject):
                    running += match if query[qi] == subject[sj] else mismatch
                    steps += 1
                    if running > best:
                        best, best_steps = running, steps
                    if best - running > xdrop:
                        break
                    qi += direction; sj += direction
                ends.append(best_steps); gains.append(best)
            left, right = ends
            key = (i-left, i+k+right, j-left, j+k+right)
            hits[key] = {'score': k*match + sum(gains),
                         'query_interval': list(key[:2]), 'subject_interval': list(key[2:])}
    return sorted(hits.values(), key=lambda hit: hit['score'], reverse=True)


def check():
    assert smith_waterman('ABCD', 'XXABCDYY')['score'] == 8
    assert smith_waterman('AAAA', 'BBBB')['score'] == 0
    assert seed_extend('ABCD', 'XXABCDYY')[0]['score'] == 8
    assert seed_extend('ABCD', 'AXCY') == []
    assert smith_waterman('ABCD', 'AXCY')['score'] > 0
    # A gap can improve the exact local alignment; ungapped extension cannot model it.
    assert smith_waterman('ABCDE', 'ABXCDE')['score'] == 8
    print(json.dumps({'exact': smith_waterman('ABCD', 'XXABCDYY'),
                      'seed_hits': seed_extend('ABCD', 'XXABCDYY'),
                      'missed_by_seeds': smith_waterman('ABCD', 'AXCY')}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    check()
