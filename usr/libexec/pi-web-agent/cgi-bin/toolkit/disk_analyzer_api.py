import os

def walk_dir(root, n_level=3):
    # Like python os.walk but can specify depth level
    # possibly useful for disk usage analyser
    #
    # Will have to see the format that either d3.js or Google graphs take
    #
    # Note: not thoroughly tested (TDD what?)

    def walk_dir_helper(root, n_level, init_level, sep):
        names = os.listdir(root)
        dirs, files = [], []

        for f in names:
            if os.path.isfile(os.path.join(root, f)):
                files.append(f)
            else:
                dirs.append(f)
            
        yield root, dirs, files

        for name in dirs:
            n_root = os.path.join(root, name)
            if (n_root.count(sep) - init_level) > n_level: break
            for x in walk_dir_helper(n_root, n_level, init_level, sep):
                yield x

    assert(n_level > 0)
    sep = os.sep
    root_level = root.count(sep)
    
    return walk_dir_helper(root, n_level, root_level, sep)

if __name__ == "__main__":
    pass
