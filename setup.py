import os
import setuptools
import subprocess
import tadman

def get_version_number(a_file):
    open_file = open(a_file)

    for a_line in open_file:
        if '__version__' in a_line:
            split_list = a_line.split()
            version_number = split_list[-1][1:-1]
            break
    open_file.close()

    return version_number

def which(a_file):
    for a_path in os.environ["PATH"].split(os.pathsep):

        test_path = os.path.join(a_path, a_file)

        if os.path.exists(test_path):
            return test_path

    else:
        return None

class InstallManpage(setuptools.Command):

    description = 'Build and Install the manpage using asciidoctor'
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        input_file = "%s/MANPAGE.adoc" % os.getcwd()
        output_file = "/usr/share/man/man8/tadman.8"

        asciidoctor_path = which('asciidoctor')

        if asciidoctor_path:
            command = [asciidoctor_path, "--backend", "manpage", "--doctype",
                       "manpage", "--out-file", output_file, input_file]

            return_value = subprocess.check_call(command)

            if return_value == 0:
                print("Tadman manpage installed at %s" % output_file)
            else:
                print("Manpage failed to build!")
        else:
            print("Asciidoctor not found in path, please install it")

setuptools.setup(
    # Package info
    name='tadman',
    description="Some package manager written in Python",
    #version = get_version_number('./tadman/__init__.py'),
    version = tadman.__version__,
    # Author and Project info
    author = "Ted Moseley",
    author_email = "tmoseley1106@gmail.com",
    url = "https://github.com/KeepPositive/Tadman",
    # File/Directory info
    packages = ["tadman"],
    scripts = ["bin/tadman-curses"],
    # Test related
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    # Docs related
    cmdclass = {
        'build_man': InstallManpage
    }
)
