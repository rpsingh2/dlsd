def a12(lst1, lst2):
  "how often is x in lst1 more than y in lst2?"
  def loop(t, t1, t2):
    while t1.j < t1.n and t2.j < t2.n:
      h1 = t1.l[t1.j]
      h2 = t2.l[t2.j]
      h3 = t2.l[t2.j + 1] if t2.j + 1 < t2.n else None
      if h1 > h2:
        t1.j += 1
        t1.gt += t2.n - t2.j
      elif h1 == h2:
        if h3 and h1 > h3:
          t1.gt += t2.n - t2.j - 1
        t1.j += 1
        t1.eq += 1
        t2.eq += 1
      else:
        t2, t1 = t1, t2
    return t.gt * 1.0, t.eq * 1.0