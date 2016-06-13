import getpass
import time

def build_logger(prefix):

    log_path = "%s/tad.log" % prefix

    with open(log_path, 'w') as log_file:

        write_list = [("Type: Build"),
                ("Time: %s" % time.strftime("%Y-%m-%d %H:%M:%S")),
                ("User: %s" % getpass.getuser())]

        for a_line in write_list:

            log_file.write("%s\n" % a_line)

        log_file.write("\n")


def install_logger(prefix, mode):

    """ The 'mode' argument is a string defining the mode just used, i.e.
    'install' or 'uninstall'.
    """

    log_path = "%s/tad.log" % prefix

    with open(log_path, 'a') as log_file:

        write_list = [("Type: %s" % mode),
                ("Time: %s" % time.strftime("%Y-%m-%d %H:%M:%S")),
                ("User: %s" % getpass.getuser())]

        for a_line in write_list:

            log_file.write("%s\n" % a_line)

        log_file.write("\n")

