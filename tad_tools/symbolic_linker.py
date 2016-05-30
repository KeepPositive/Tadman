import os

def sym_farm(start_dir, end_dir):
    """ This function walks through a directory, and recreates its structure
    by recreating the subdirectories within the root directory. For each file,
    it creates a symlink to the file within the directories created. Thus, the
    entire file structure is recreated within the root.
    """
    
    #print("Creating directory %s" % start_dir)
    
    for root, dirs, files in os.walk(start_dir):

        sub_length = len(start_dir)
       
        # For each subdirectory within the starting directory
        for name in dirs:
            
            sub_fold = os.path.join(root, name)[sub_length:]
            new_fold = "%s%s" % (end_dir, sub_fold)

            if not os.path.isdir(new_fold):
                os.mkdir(new_fold)
                print("Creating directory %s" % new_fold)
            else:
                print("Directory %s already exists" % new_fold)
        # For each file within the starting directory
        for name in files:
            
            rel_path = os.path.join(root, name)
            abs_path = os.path.abspath(rel_path)
            new_path = "%s%s" % (end_dir, rel_path[sub_length:])

            os.symlink(abs_path, new_path) 
            print("Linking %s -> %s" % (new_path, abs_path))

        print()
