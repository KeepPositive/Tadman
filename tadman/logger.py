import getpass
import time

def build_logger(a_path):

    log_path = "%s/tad.log" % a_path

    with open(log_path, 'w') as log_file:

        write_list = [("Mode: Build"),
                      ("Time: %s" % time.strftime("%Y-%m-%d %H:%M:%S")),
                      ("User: %s" % getpass.getuser())]

        for a_line in write_list:
            log_file.write("%s\n" % a_line)

        log_file.write("\n")

def install_logger(a_path, mode):

    """ The 'mode' argument is a string defining the mode just used, i.e.
    'install' or 'uninstall'.
    """

    log_path = "%s/tad.log" % a_path

    with open(log_path, 'a') as log_file:

        write_list = [("Mode: %s" % mode),
                      ("Time: %s" % time.strftime("%Y-%m-%d %H:%M:%S")),
                      ("User: %s" % getpass.getuser())]

        for a_line in write_list:

            log_file.write("%s\n" % a_line)

        log_file.write("\n")
