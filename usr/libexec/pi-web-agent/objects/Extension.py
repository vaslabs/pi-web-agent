from framework import requestDefinition
class Extension(object):
    
    def __init__(self, extensionID):
        self.extensionID = extensionID
        self.definition = requestDefinition(self.extensionID)
