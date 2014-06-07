#!/usr/bin/python
from update import *

class UpdateManagerAPI(UpdateManager):
    def getJS(self):
        update_info, returncode = update_check_quick()
        update_json = {}
        if returncode == UPDATE_PENDING:
            update_json['status'] = UPDATE_PENDING
            return update_json
        elif returncode == UPDATE_READY or returncode == NO_ACTION:
            update_json['status'] = 0
            return update_json

        update_json['packages'] = {}

        for package_entry in update_info.split("\n"):
            package_name=parse_package_name(package_entry)
            if package_name == None:
                continue
            description=parse_package_description(package_entry)

            update_json['packages'][package_name] = description

        return update_json



def main():
    form = cgi.FieldStorage()
    if (getAptBusy()):
      js_status = {"status":PROCESS_PENDING}
      composeJS(json.dumps(js_status))
      return
    updMgr = UpdateManagerAPI()

    composeJS(updMgr.getJS())
    
    
if __name__ == '__main__':
    main()
