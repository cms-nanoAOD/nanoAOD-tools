

class ComponentContainer:
    def __init__(self, name, dataset, xsec=0):
        self.name         = name        
        self.dataset      = dataset  
        self.options      = {} 
        self.options['xsec'] = xsec
