import json

class FileSystemObject(object):

    def __init__(self, name, parent, size, children):
        # name :: str
        # parent :: str - parent's name not ref to parent
        # size :: int
        # children :: List[FileSystemObject]
        self.name = name
        self.parent = parent
        self.size = size
        self.children = children

        
class DefaultEncoder(json.JSONEncoder):

    def default(self, o):
        return o.__dict__


def traverse_fs(root, parent="", n_levels=3):
    # root :: str
    # parent :: str
    # n_level :: int
    #
    # for now ignore n_levels
    from os.path import getsize
    from os.path import join
    
    names = os.listdir(root)
    dirs, files = list(), list()
    
    for f in names:
        if os.path.isfile(join(root, f)):
            files.append(f)
        else:
            dirs.append(f)

    children = list(FileSystemObject(f, root, getsize(join(root, f)), list()) for f in files)

    for name in dirs:
        n_root = join(root, name)
        children.append(traverse_fs(root=n_root, parent=root))
    
    dir_size = sum(f.size for f in children)

    return FileSystemObject(root, parent, dir_size, children)

    
def get_chart_format(root_dir):
    # root_dir :: FileSystemObject
    from collections import deque
    
    to_process = deque()
    entry_list = list()
    
    to_process.append(root_dir)
    while to_process:
        f = to_process.popleft()
        entry_list.append([f.name, f.parent, f.size])

        for child in f.children:
            to_process.append(child)

    return entry_list

    
def main_test():
    root_dir = traverse_fs("/Users/argyris/workspace/dir_test/dir1/")
    entry_list = get_chart_format(root_dir)
    entry_list_json = DefaultEncoder().encode(entry_list)
    
    return entry_list_json
