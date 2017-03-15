import pytest

from tadman import path_tools

def test_ending_slash_removal():
    
    tests = ['/home/squid', '/path/to/something/', '/var/lib/foo/bar']
    results = ['/home/squid', '/path/to/something', '/var/lib/foo/bar']
    
    for x in range(len(tests)):
        assert path_tools.last_slash_check(tests[x]) == results[x]

def test_name_version_split():

    test_names = ['openbox-3.6.1', 'htop']
    results = [('openbox', '3.6.1'), ('htop', '')]

    for y in range(len(test_names)):
        assert path_tools.name_version_split(test_names[y]) == results[y]
