import sort as s

def defAlphabetOrd(c):
    """
    default ascii values, so [0-127]
    :return:
    """
    return ord(c)

def genSA_LCP(corpus,order=defAlphabetOrd,radix=128):
    """
    Generates the Suffix Array and LCP array for the corpus.
    Should be O(size(corpus)) time. Algorithm based off of lecture notes from
    https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-851-advanced-data-structures-spring-2012/calendar-and-notes/MIT6_851S12_Lec16.pdf

    :param corpus: a large string
    :return: the tuple (SA, LCP), where
        SA: the suffix array
        LCP: the LCP array
    """
    #sort the alphabet
        #this step done by the client

    #replace each letter by its rank in the alphabet
    new_t = [order(c) for c in corpus]

    #form T_0 (list of symbols, each symbol is 3 consecutive letters concatenated)
    T_0 = [new_t[3*k]*radix*radix + new_t[3*k+1]*radix+new_t[3*k+2]
           for k in range(len(new_t))]

    #form T_1
    #form T_2