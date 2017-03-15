# Standard
import os
# Project
from tadman import autotools

def get_file_contents(a_file):

    contents = []
    open_file = open(a_file)

    for x in open_file:
        contents.append(x)

    return contents

def test_first_occurance():

    in_file = get_file_contents(os.path.abspath("tests/data/configure1.txt"))

    occurance = autotools.find_first(in_file, 'Optional Features:\n')

    assert occurance == 67


