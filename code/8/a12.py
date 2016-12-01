def a12slow(lst1,lst2):
  "how often is x in lst1 more than y in lst2?"
  more = same = 0.0
  for x in lst1:
    for y in lst2:
      if    x == y : same += 1
      elif  x >  y : more += 1
  x= (more + 0.5*same) / (len(lst1)*len(lst2))
  return x