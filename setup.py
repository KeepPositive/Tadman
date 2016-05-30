from setuptools import setup

setup( 
    # Package info
    name='tadman',
    description="Some package manager written in Python",
    version = "0.0.1",
    install_requires = ['Click'],
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

    #entry_points = {
    #    "console_scripts": ['tadman = tad_main.main:main']}
) 
