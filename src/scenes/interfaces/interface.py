class Interface(object):
    
    def interface(self):
        """ Returns an interface element hierarchy 
        It should be overrided
        """
        pass

    def resize(self):
        """ Adjusts the size according to the orientation 
        It may be overrided
        """
        pass

    def create_interface(self):
        self.extract_fields(self.interface())
        self.resize()

    def extract_fields(self, element):
        """ Create fields for each .name field in the object hierchachy """
        if not element:
            return None
        if element.name:
            setattr(self, element.name, element)
        for child in element.children:
            self.extract_fields(child)
