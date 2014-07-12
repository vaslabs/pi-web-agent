from live_info import package_is_installed
from Extension import Extension
class DependableExtension(Extension):
        
    '''
    check if required dependencies are installed
    '''
    def check_status(self):
        for dependency in self.definition['dependencies']:
            if (not package_is_installed(dependency)):
                return False
        return True
        
        
    def getStatusJS(self):
        data = { 'name': self.definition['title'],\
                 'status': self.check_status()}
        return data

    '''
    Call it inside an Extension. This module does not include
    the module required for the composeJS intentionally because
    it is an abstract implementation
    '''       
    def output_status(self):
        self.composeJS(getStatusJS())
