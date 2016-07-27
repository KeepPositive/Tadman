import os
import setuptools
import subprocess

def which(a_file):
    for a_path in os.environ["PATH"].split(os.pathsep):

        test_path = os.path.join(a_path, a_file)

        if os.path.exists(test_path):
            return test_path

    else:
        return False

setuptools.setup(
    # Package info
    name='tadman',
    description="Some package manager written in Python",
    version = "0.1.0",
    # Author and Project info
    author = "Ted Moseley",
    author_email = "tmoseley1106@gmail.com",
    url = "https://github.com/KeepPositive/Tadman",
    # File/Directory info
    packages = ["tadman"],
    scripts = ["bin/tadman-curses"])


# Documentation related stuff
input_file = "%s/docs/tadman.man.adoc" % os.getcwd()
output_file = "/usr/share/man/man8/tadman.8"

adoc = which('asciidoctor')

if adoc:
    subprocess.call([adoc, "--backend", "manpage", "--doctype", "manpage",
                     "--out-file", output_file, input_file])

    print("Tadman manpage installed at %s" % output_file)
else:
    print('%s not found in path, please install it' % a_file)
