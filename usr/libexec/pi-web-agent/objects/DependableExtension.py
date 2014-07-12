from live_info import package_is_installed, getAptBusy
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
        
    def _generateMissingDependenciesView(self):
        if ( getAptBusy( ) ):
            html = "<div>It seems that the dependencies of this package are not installed but the OS package manager is busy now. Try again in a moment...</div>"
        else:
            html = "<div>The dependencies of this module are missing. Do you want to install them?</div><br/><button onclick=\"getDependenciesFor('" +\
                    self.extensionID + "')\">Resolve dependencies</button>"
        return html
