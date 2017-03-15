# Standard
import os
import subprocess
# Dependency
import docutils.core
import docutils.writers
import setuptools
# Project
import tadman


def parse_manpage(string):

    return docutils.core.publish_string(source=string,
                                        writer_name="manpage")


class InstallManpage(setuptools.Command):

    description = "Build manpage using docutils and install it"
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        input_file = os.path.abspath("tadman-curses.8.rst")
        output_file = "/usr/share/man/man8/tadman-curses.8"

        with open(input_file) as a_file:
            print("Opening reStructuredText file {}".format(input_file))
            contents = a_file.read()

        processed = parse_manpage(contents)
        print("Processed manpage file using docutils")

        with open(output_file, 'w') as a_file:
            print("Writing output file {}".format(output_file))
            a_file.write(processed.decode())

        print("Manpage installed!")


setuptools.setup(
    name='tadman',
    description="Some package manager written in Python",
    version = tadman.__version__,
    author = "Ted Moseley",
    author_email = "tmoseley1106@gmail.com",
    url = "https://gitlab.com/Tad-OS/Tadman",
    packages = ["tadman"],
    scripts = ["bin/tadman-curses"],
    # For the manpage command
    cmdclass = {
        "install_manpage": InstallManpage
    }
)
