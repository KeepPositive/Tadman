def path_mop(a_path):

    """ Occasionally, a user may enter a path which is suffixed with a '/'
    (which is not POSIX-y, so shame on them). So, we can not rely on the
    os.path.basename module to get the name of the package. So, this module
    does this correctly automagically.

    Returns the name of the package, which can either be the basename of path,
    or the phrase before the last slash.
    """

    path_split = a_path.split(sep='/')
    
    if a_path[-1] == '/':
        package_name = path_split[-2]
    else:
        package_name = path_split[-1]

    return package_name

def version_removal(in_name):

    """ This script tries it's best to remove the package naming filth from the
    name of the package found using the path_mop function.

    Returns the (likely) name of the package.
    """

    out_name = ()
    name_split = in_name.split(sep='-')
    
    if '-' in in_name:
        for x in reversed(range(len(name_split))):
            if name_split[x][0].isdigit():
                start_index = in_name.find(name_split[x])
                out_name = in_name[:(start_index - 1)]
    else:
        out_name = in_name

    return out_name

def main_filter(a_name):

    """ This just combines the scripts above into a nice main function. """

    raw_name = path_mop(a_name)
    just_name = version_removal(raw_name)

    return(just_name)
