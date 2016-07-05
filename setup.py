import os
import setuptools
import subprocess
import sys

def which(a_file):
    for a_path in os.environ["PATH"].split(os.pathsep):

        test_path = os.path.join(a_path, a_file)

        if os.path.exists(test_path):
            return test_path

    else:
        print('%s not found in path, please install it' % a_file)
        sys.exit(0)

setuptools.setup(
    # Package info
    name='tadman',
    description="Some package manager written in Python",
    version = "0.0.3",
    # Author and Project info
    author = "Ted Moseley",
    author_email = "tmoseley1106@gmail.com",
    url = "https://github.com/KeepPositive/Tadman",

    # File info
    packages = ["tad_autotools",
                "tad_cmake",
                "tad_interface",
                "tad_tools"],

    scripts = ["tadman"])


# Documentation related stuff
try:

    input_file = "%s/docs/tadman.man.adoc" % os.getcwd()
    output_file = "/usr/share/man/man8/tadman.8"

    adoc = which('asciidoctor')

    subprocess.call([adoc, "--backend", "manpage", "--doctype", "manpage",
                     "--out-file", output_file, input_file])

    print("Tadman manpage installed at %s" % output_file)
