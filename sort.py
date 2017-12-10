def radixsort( aList ,RADIX=10, maxLength = None):
  """
  In-place radix sort
  This code inspired by http://www.geekviewpoint.com/python/sorting/radixsort
  :param aList: the list to be sorted in place.
                Assumes all integers
  :return: none
  """
  if(maxLength is None):
    maxLengthReached = False #denotes if we are currently comparing digits at the last positions
    tmp , place_value = -1, 1

    while not maxLengthReached:
      maxLengthReached = True
      # declare and initialize buckets
      buckets = [list() for _ in range( RADIX )]

      # split aList between lists
      for  d in aList:
        tmp = d // place_value
        buckets[tmp % RADIX].append( d )
        if maxLengthReached and tmp > 0:
          maxLengthReached = False

      # empty lists into aList array
      a = 0
      for b in range( RADIX ):
        buck = buckets[b]
        for d in buck:
          aList[a] = d
          a += 1

      # move to next digit
      place_value *= RADIX
  else:
    place_value = 1
    for place in range(maxLength):
      # declare and initialize buckets
      buckets = [list() for _ in range(RADIX)]

      # split aList between lists
      for d in aList:
        buckets[ (d // place_value) % RADIX].append(d)

      # empty lists into aList array
      a = 0
      for b in range(RADIX):
        buck = buckets[b]
        for d in buck:
          aList[a] = d
          a += 1

      # move to next digit
      place_value *= RADIX
