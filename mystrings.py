class MyString:
    def __init__(self, data,excl=None):
        """
        :param data: the raw string
        :param excl: the list of exclusions in data
                each element is of form [a,b), and
                if list is [ ... [a1,b1), ... , [a2,b2), ... ]
                then a1 < b1 < a2
        """
        self.data = data
        self.list_excl = excl

    @classmethod
    def fromSplice(cls,ms,start,stop):
        """
        :param ms: MyString instance
        :param start: ui start of the splice, must be strictly less than the stop
        :param stop: ui stop of the splice
        :return: new MyString instance, with the same data as ms (should not be a copy of data, but the same pointer).
            Spliced from [(ui)start,(ui)stop), with any exclusions
        """
        news = cls(ms.data,ms.list_excl)
        news.addExcl()
        #return cls(ms.data,[start,stop])

    def addExcl(self,start,stop,excl_start,excl_stop):
        """
        new excluded interval is [(raw)start,(raw)stop),
        this function places the new excl interval in the list_excl

        :param start: the raw index of the excl start
        :param stop: the raw index of the excl stop
        :param excl_start: the index of the interval that is right after start
        :param excl_stop: the index of the interval that is right after stop
        :return: None
        """
        if(stop<=start): raise IndexError
        if(excl_start<excl_start): raise IndexError
        if(self.list_excl[excl_start][0]<=start): raise IndexError
        if(excl_stop!=len(self.list_excl) and self.list_excl[excl_stop][0]<=stop): raise IndexError

        self.list_excl = self.list_excl[:excl_start] + self.list_excl[excl_stop:]
        self.list_excl.insert(excl_start,[start,stop])

    def getUserChar(self,ui):
        """
        :param ui: the user index, i.e. the index of the char as if we had called toString
        :return: the char at ui (skipping any excluded regions)
        """
        rit = 0  # index of the current raw char
        uit = -1  # index of the current user chars we've seen
        eit = 0  # index of the excluded region right after rit (rit might be the first char in list_excl[eit] )
        while (rit < len(self.data)):
            if (rit >= self.list_excl[eit][0]):
                rit = self.list_excl[eit][1]
                eit += 1
            if (rit >= len(self.data)): raise IndexError
            uit += 1 #we seen another user char
            if(uit==ui): return self.data[rit]
            rit += 1
        raise IndexError #if ui is valid, we should never get here
    def getUserCharStartingFrom(self,ui,rin=0,uin=0,ein=0):
        """
        NOTE: this function DOES NOT VERIFY if the following assumptions are correct
        :param ui: the user index we want to get
        :param rin: the starting raw index we look from
        :param uin: the starting user index we look from (that
        :param ein:
        :return:
        """

    def getUserCharAfterRaw(self,rawi,excli):
        """
        :param rawi: the raw index provided
        :param excli: the index of the excluded interval right after rawi or that contains rawi
        :return: the user char after the raw index, or None if there is no user char after rawi
        """
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
            if(rit>=self.list_excl[eit][0]):
                rit=self.list_excl[eit][1]
                eit+=1
            if(rit>=len(self.data)): break
            l.append(self.data[rit])
            rit+=1
        return ''.join(l)