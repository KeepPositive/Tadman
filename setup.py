import os
import setuptools
import subprocess

setuptools.setup( 
    # Package info
    name='tadman',
    description="Some package manager written in Python",
    version = "0.0.2",
    # Author and Project info
    author = "Ted Moseley",
    author_email = "tmoseley1106@gmail.com",
    url = "https://github.com/KeepPositive/Tadman",
    
    # File info
    packages = ["tad_autotools", 
                "tad_cmake",
                "tad_interface",
                "tad_tools"],

    scripts = ["tadman"]
)

try:

    input_file = "%s/docs/tadman.man.adoc" % os.getcwd() 
    output_file = "/usr/share/man/man8/tadman.8"

    subprocess.call(["asciidoctor", "--backend", "manpage",
                     "--doctype", "manpage", 
                     "--out-file", output_file, 
                     input_file])

except FileNotFoundError:
    print("Documentation not installed. Please install Asciidoctor")
else:
    print("Tadman manpage installed at %s" % output_file)
