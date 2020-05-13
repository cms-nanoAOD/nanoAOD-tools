class variabile(object):
    def __init__(self, name, title, taglio, nbins, xmin, xmax):
        self._name=name
        self._title=title
        self._taglio=taglio
        self._nbins=nbins
        self._xmin=xmin
        self._xmax=xmax

    def __str__(self):
        return  '\"'+str(self._name)+'\",\"'+str(self._title)+'\",\"'+str(self._taglio)+'\",'+str(self._nbins)+','+str(self._xmin)+','+str(self._xmax)

