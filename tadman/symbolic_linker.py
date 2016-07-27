# Standard
import os

def sym_farm(package_path):

    """ This function walks through a directory, and recreates its structure
    by recreating the subdirectories within the root directory. For each file,
    it creates a symlink to the file within the directories created. Thus, the
    entire file structure is recreated within the root.
    """

    start_dir = package_path

    for root, dirs, files in os.walk(start_dir):

        sub_length = len(start_dir)
        # For each subdirectory within the starting directory
        for name in dirs:

            sub_fold = os.path.join(root, name)[sub_length:]

            if not os.path.isdir(sub_fold):
                os.mkdir(sub_fold)
                print("Created directory %s" % sub_fold)

            else:
                print("Directory %s already exists" % sub_fold)

        # For each file within the starting directory
        for name in files:

            if name == 'tad.log':
                continue

            rel_path = os.path.join(root, name)
            abs_path = os.path.abspath(rel_path)
            new_path = rel_path[sub_length:]
            try:
                os.symlink(abs_path, new_path)
                print("%s --> %s" % (new_path, abs_path))
            except FileExistsError:
                print("File %s already exists" % new_path)

def sym_reap(package_path):

    """
     This function removes any exisiting links that were created by the
    sym_farm function while installing a package. It is almost like
    uninstall the package so to speak.

    This function does not return anything.
    """

    unlink_path = package_path
    sub_length = len(unlink_path)

    for root, dirs, files in os.walk(unlink_path):
        # For each file within the starting directory
        for name in files:

            if name == 'tad.log':
                continue

            rel_path = os.path.join(root, name)
            abs_path = os.path.abspath(rel_path)
            new_path = abs_path[sub_length:]

            if os.path.islink(new_path):
                os.remove(new_path)
                print("%s -X> %s" % (new_path, abs_path))
            else:
                print("File %s is not a link" % new_path)

    # For each subdirectory within the starting directory
    for root, dirs, files in os.walk(unlink_path):
        directory_list = []

        for name in dirs:

            sub_fold = os.path.join(root, name)
            new_fold = sub_fold[sub_length:]

            directory_list.append(new_fold)

        for directory in directory_list:

            if not os.path.isdir(directory):
                print("Directory %s does not exist" % directory)
            elif os.listdir(directory) != []:
                print("Directory %s is not empty" % directory)
            else:
                os.rmdir(directory)
                print("Removing directory %s" % directory)
