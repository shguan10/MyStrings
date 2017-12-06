class MyString:
    def __init__(self, data,excl=None,spliceStart=None,spliceEnd=None):
        """
        :param data: the raw string
        :param excl: the list of exclusions in data
                each element is of form [a,b), and
                if list is [ ... [a1,b1), ... , [a2,b2), ... ]
                then a1 < b1 < a2.
                in other words, there are no redundant intervals in excl
        :param spliceStart: rstart of the splice (no user chars exists before rstart, exclusive)
        :param spliceEnd: rend of the splice (no user chars exist after rend, inclusive)
        """
        self.data = data
        self.list_excl = excl
        self.spliceStart=spliceStart#TODO unused
        self.spliceEnd = spliceEnd

    @classmethod
    def fromSplice(cls,ms,rstart,rstop):
        """
        :param ms: MyString instance
        :param rstart: ri start of the splice, must be strictly less than the stop
        :param rstop: ri stop of the splice
        :return: new MyString instance, with the same data as ms (should not be a copy of data, but the same pointer).
            Spliced from [(ri)rstart,(ri)rstop), with any exclusions
        """
        #TODO finish
        raise NotImplementedError
        #news = cls(ms.data,ms.list_excl)
        #news.addExcl()
        #return cls(ms.data,[start,stop])

    def addExcl(self, rnew_excl_start, rnew_excl_stop, old_adj_excl_start, old_adj_excl_stop):
        """
        new excluded interval is [(raw)rstart,(raw)stop),
        this function places the new excl interval in the list_excl, deleting any obsolete intervals if needed

        :param rnew_excl_start: the raw index of the splice start
        :param rnew_excl_stop: the raw index of the splice stop
        :param old_adj_excl_start: the index of the excl interval that is right after rnew_excl_start
        :param old_adj_excl_stop: the index of the excl interval that is right after rnew_excl_stop
        :return: None
        """
        if(rnew_excl_stop<=rnew_excl_start): raise IndexError
        if(old_adj_excl_stop<old_adj_excl_start): raise IndexError
        if(old_adj_excl_start<len(self.list_excl) and old_adj_excl_stop<len(self.list_excl)):
            if(self.list_excl[old_adj_excl_start][0]<=rnew_excl_start): raise IndexError
            if(old_adj_excl_stop!=len(self.list_excl) and self.list_excl[old_adj_excl_stop][0]<=rnew_excl_stop): raise IndexError

        self.list_excl = self.list_excl[:old_adj_excl_start] + self.list_excl[old_adj_excl_stop:]
        self.list_excl.insert(old_adj_excl_start, [rnew_excl_start, rnew_excl_stop])

    def findTokFromRaw(self,tok,rstart=0, excl_start=0):
        """
        this function DOES NOT check if the following assumptions hold
            accepts:
                tok: the substring to find
                rstart: the rindex of the starting look index
                excl_start: the index of the first interval after rstart (at first, rstart may be in this interval)

            returns:
                (tstart,tend,lo,hi):
                    tstart: the index of the position of the first occurence of tok in self.data, if it exists, otherwise -1
                    tend: the index after the last char of the first occurnece of tok in self.data
                    lo: index of the first interval after tstart
                    hi: index of the first interval after tend
        """
        exc_index = excl_start #index of the excluded interval right after str_index
        str_index = rstart #when accessing the instr through str_index, str_index should not be in one of the intervals in the list_excl
        tok_len = len(tok)
        str_len = len(self.data)
        list_len = len(self.list_excl)
        found = False
        while(str_index <= (str_len - tok_len) and not found):
            # check if we need to skip any excluded intervals
            #NOTE: if the list_excl is in the right format, we should not need to check this more than once
            if(exc_index<list_len and str_index >= self.list_excl[exc_index][0]):
                #instr[str_index] is in the excluded interval
                str_index = self.list_excl[exc_index][1] #this might be the str_len
                exc_index+=1
            #str_index is not in an excluded interval
            if(str_index<str_len and tok[0]==self.data[str_index]):
                tok_index= 0
                poten = True
                str_look_index = str_index
                exc_look_index = exc_index
                while(tok_index<tok_len and str_look_index<str_len and poten):
                    #check if we need to skip any excluded intervals
                    if(exc_look_index<list_len and str_look_index >= self.list_excl[exc_look_index][0]):
                        #instr[str_look_index] is in the excluded interval
                        str_look_index = self.list_excl[exc_look_index][1]
                        exc_look_index += 1
                    #str_look_index is not in an excluded interval
                    if(str_look_index >= str_len or tok[tok_index]!=self.data[str_look_index]):
                        poten = False
                    tok_index+=1
                    str_look_index += 1
                found = (poten and tok_index == tok_len)
                if(found): return (str_index,str_look_index,exc_index,exc_look_index)
            str_index +=1
        if(found): raise ValueError #this statement should not be reached
        else: return (-1,-1,-1,-1)

    def getUserChar(self,ui):
        """
        Inefficient algorithm that starts from the first char and iterates through the raw string until we see ui
        :param ui: the user index, i.e. the index of the char as if we had called toString
        :return: the char at ui (skipping any excluded regions)
        """
        #TODO does not consider splices
        rit = 0  # index of the current raw char
        uit = -1  # index of the current user chars we've seen
        eit = 0  # index of the excluded region right after rit (at first, rit might be the first char in list_excl[eit] )
        while (rit < len(self.data)):
            if (rit >= self.list_excl[eit][0]):
                rit = self.list_excl[eit][1]
                eit += 1
            if (rit >= len(self.data)): raise IndexError
            uit += 1 #we've seen another user char
            if(uit==ui): return self.data[rit]
            rit += 1
        raise IndexError #if ui is valid, we should never get here

    def getUserCharStartingFrom(self,ui,rin=-1,uin=0,ein=0):
        """
        NOTE: this function DOES NOT VERIFY if the following assumptions are correct
        :param ui: the user index we want to get
        :param rin: the starting raw index we look from
        :param uin: the number of user chars we see if we look from data[0,rin] inclusive
        :param ein: index of the excluded region right after rit (at first, rit might be the first char in list_excl[ein] )
        :return: the char at ui (skipping any excluded regions)
        """
        # TODO does not consider splices
        rit = rin  # index of the current raw char
        uit = uin  # index of the current user chars we've seen
        eit = ein  # index of the excluded region right after rit (at first, rit might be the first char in list_excl[eit] )
        while (rit < len(self.data)):
            if (rit >= self.list_excl[eit][0]):
                rit = self.list_excl[eit][1]
                eit += 1
            if (rit >= len(self.data)): raise IndexError
            uit += 1 #we seen another user char
            if(uit==ui): return self.data[rit]
            rit += 1
        raise IndexError #if ui is valid, we should never get here

    def getUserCharAfterRaw(self,rawi,excli):
        """
        :param rawi: the raw index provided
        :param excli: the index of the excluded interval right after rawi or that contains rawi
        :return: the user char after the raw index, or None if there is no user char after rawi
        """
        # TODO does not consider splices
        if(self.list_excl[excli][0]>rawi):#rawi is right before the excli
            if(excli>0 and self.list_excl[excli-1][1]>rawi): raise IndexError
            ui = rawi + 1
            if(self.list_excl[excli][0] > ui): return self.data[ui]
            else:
                ui = self.list_excl[excli][1]
                if (ui >= len(self.data)): return None
                return self.data[ui]
        elif(self.list_excl[excli][0]<=rawi<self.list_excl[excli][1]):#rawi is within excli
            ui = self.list_excl[excli][1]
            if (ui >= len(self.data)): return None
            return self.data[ui]
        else: raise IndexError

    def toString(self):
        l = []
        rit = 0 #index of the current raw char
        eit = 0 #index of the excluded region right after rit (rit might be the first char in list_excl[eit] )
        while(rit < len(self.data)):
            if(eit<len(self.list_excl) and rit>=self.list_excl[eit][0]):
                rit=self.list_excl[eit][1]
                eit+=1
            if(rit>=len(self.data)): break
            l.append(self.data[rit])
            rit+=1
        return ''.join(l)