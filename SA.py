import sort as s

def defAlphabetOrd(c):
    """
    default ascii values, so [0-127]
    Assume the null terminator '\0' is not in the alphabet
    :return:
    """
    return ord(c)


def genSA_LCP(corpus,order=defAlphabetOrd,radix=128):
    """
    Generates the Suffix Array and LCP array for the corpus.
    Should be O(size(corpus)) time. Algorithm based off of lecture notes from
    https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-851-advanced-data-structures-spring-2012/calendar-and-notes/MIT6_851S12_Lec16.pdf

    :param corpus: a large string
    :param order: function that returns the rank of a char in sorted alphabet
    :param radix: size of the alphabet
    :return: the tuple (SA, LCP), where
        SA: the suffix array
        LCP: the LCP array
    """
    #sort the alphabet
        #this step done by the client

    #replace each letter by its rank in the alphabet
    new_t = [order(c) for c in corpus]

    #create SA_12



    #form T_0 (list of symbols, each symbol is 3 consecutive letters concatenated)
    #TODO is my implementation of out-of-bounds correct? need to reference original paper
    T_0 = [
        new_t[3*k]*radix*radix +
        (new_t[3*k+1]*radix if 3*k+1 <len(new_t) else 0)+
        (new_t[3*k+2] if 3*k+2 <len(new_t) else 0)
           for k in range(len(new_t)//3)
    ]

    #form T_1
    T_1 = [
        (new_t[3*k+1]*radix*radix if 3*k+1 <len(new_t) else 0)+
        (new_t[3*k+2]*radix if 3*k+2 <len(new_t) else 0)+
        (new_t[3*k+3] if 3*k+3 <len(new_t) else 0)
           for k in range(len(new_t)//3)
    ]

    #form T_2
    T_2 = [
        (new_t[3 * k + 2] * radix * radix if 3 * k + 2 < len(new_t) else 0) +
        (new_t[3 * k + 3] * radix if 3 * k + 3 < len(new_t) else 0) +
        (new_t[3 * k + 4] if 3 * k + 4 < len(new_t) else 0)
            for k in range(len(new_t)//3)
    ]

    #recurse on <T_0, T_1>

"""
BELOW IS DIRECTLY PORTED FROM C++ 
PROVIDED IN Karkkainen and Sanders ICLP 2003
"""
def leq_pairs(a1, a2, b1, b2):
    """
    helper function
    :param a1: int
    :param a2: int
    :param b1: int
    :param b2: int
    :return: bool
    """
    return (a1<b1 or a1==b1 and a2<=b2)

def leq_triples(a1, a2, a3, b1, b2, b3):
    """
    accepts all ints,
    returns a bool
    """
    return (a1<b1 or a1==b1 and leq_pairs(a2,a3,b2,b3))

def radixPass(a, b, r, n, K):
    """
    stably sort a[0..n-1] to b[0..n-1] with keys in 0..K from r
    :param a: in-list of int
    :param b: out-list of int
    :param r: list of int, sorted alphabet of a and b
    :param n: length of lists a and b
    :param K: largest key in the alphabet (int)
    :return: sorts list b in-place
    """
    counter_array = [0 for _ in range(K + 1)]

    # count occurrences
    for i in range(n): counter_array[r[a[i]]] += 1

    # exclusive prefix sums
    psum = 0
    for i in range(K + 1):
        t = counter_array[i]
        counter_array[i] = psum
        psum += t

    for i in range(n):
        counter_array[r[a[i]]] += 1
        b[counter_array[r[a[i]]]] = a[i]

def suffixArray(s, SA, n, K):
    """
    find the suffix array SA of s[0..n-1] in {1..K}^n
    requires s[n] = s[n+1] = s[n+2] = 0, n>=2
    :param s: int list
    :param SA: int list
    :param n: int
    :param K: int
    :return:
    """
    n0 = (n + 2) // 3
    n1 = (n + 1) // 3
    n2 = n // 3
    n02 = n0 + n2
    s12 = [0 for _ in range(n02 + 3)]
    SA12 = [0 for _ in range(n02 + 3)]
    s0 = [0 for _ in range(n0)]
    SA0 = [0 for _ in range(n0)]

    # generate positions of mod 1 and mod 2 suffixes
    # the "+(n0-n1)" adds a dummy mod 1 suffix if n%3 ==1
    j=0
    for i in range(n+(n0-n1)):
        if(i%3 != 0):
            s12[j]=i
            j+=1

    #lsb radix sort the mod 1 and mod 2 triples
    radixPass(s12, SA12, s+2, n02,K) #TODO set these up with buffers
    radixPass(SA12, s12, s+1, n02, K)
    radixPass(s12, SA12, s, n02, K)

    #find lexicographic names of triples
    name , c0, c1, c2 = 0, -1, -1, -1
    for i in range(n02):
        if(s[SA12[i]]!=c0 or s[SA12[i] +1]!= c1 or s[SA12[i]+2]!=c2):
            name+=1
            c0=s[SA12[i]]
            c1=s[SA12[i]+1]
            c2=s[SA12[i]+2]
        if(SA12[i]%3 ==1): s12[SA12[i]//3] = name #left half
        else: s12[SA12[i]//3+n0] = name #right half

    #recurse if names are not yet unique
    if(name < n02):
        suffixArray(s12,SA12,n02,name)
        #store unique names in s12 using the suffix array
        for i in range(n02): s12[SA12[i]] = i+1
    else: #generate the suffix array of s12 directly
        for i in range(n02): SA12[s12[i]-1] = i

    #stably sort the mod 0 suffixes from SA12 by their first char
    j=0
    for i in range(n02):
        if(SA12[i]<n0):
            s0[j]=3*SA12[i]
            j+=1
    radixPass(s0,SA0, s, n0,K)

    #merge the sorted SA0 suffixes and sorted SA12 suffixes
    t = n0-n1
    p=0
    for k in range(n):
        #define GetI() (SA12[t] < n0 ? SA12[t]*3 +1 : (SA12[t]-n0)*3 +2)
        #pos of current offset 12 suffix
        i = SA12[t]*3 +1 if SA12[t] < n0 else (SA12[t]-n0)*3 +2

        #pos of current offset 0 suffix
        j = SA0[p]

        if(SA12[t]<n0):
            SA12_is_smaller =leq_pairs(s[i], s12[SA12[t]+n0], s[j], s12[j//3])
        else:
            SA12_is_smaller =leq_triples(s[i],s[i+1], s12[SA12[t]-n0+1], s[j], s[j+1],s12[j//3+n0])

        if(SA12_is_smaller):
            SA[k] = i
            t+=1
            if(t==n02): #done --- only SA0 suffixes left
                k+=1
                while(p<n0):
                    SA[k]=SA0[p]
                    p+=1
                    k+=1
        else:
            #suffix from SA0 is smaller
            SA[k] = j
            p+=1
            if(p==n0): #done -- only SA12 suffixes left
                k += 1
                while (t < n02):
                    SA[k] = SA12[t]*3 +1 if SA12[t] < n0 else (SA12[t]-n0)*3 +2#
                    t += 1
                    k += 1
        return #SA should be sorted in place now