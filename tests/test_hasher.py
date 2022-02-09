import getpass
from pathlib import Path
import platform
import pytest
from src.hasher.hasher import Hasher


class TestHasher:

    def test_hasher_exists(self):
        h = Hasher
        assert h is not None
        assert h.default_hash_type() == 'sha256'

    def test_hasher_constructor(self):
        h = Hasher()
        assert h is not None
        assert h.default_hash_type() == 'sha256'
        assert h._hash_type == 'sha256'

    def test__normalise_hash_type(self):
        validtype = 'sha256'
        invalidtype = 'blahblah'
        nonsense = 42

        out = Hasher._normalise_hash_type(validtype)
        assert out == validtype

        with pytest.raises(Exception):
            out = Hasher._normalise_hash_type(invalidtype)

        with pytest.raises(Exception):
            out = Hasher._normalise_hash_type(nonsense)

        with pytest.raises(Exception):
            out = Hasher._normalise_hash_type()

        with pytest.raises(Exception):
            out = Hasher._normalise_hash_type('')

    def test_file_exists(self):
        afile = Path(r"..\testdata\test1\subfolder1\testfile.txt")
        afolder = Path(r"..\testdata\test1\subfolder1")
        nonexistentfile = Path(r"..\testdata\test1\subfolder1\blahblah.txt")
        nonexistentfolder = Path(r"..\testdata\test1\subfolder1blahblah")

        h = Hasher()
        h._source = afile
        out = h._file_or_folder()
        assert out == 'file'

        h = Hasher()
        h._source = afolder
        out = h._file_or_folder()
        assert out == 'folder'

        with pytest.raises(FileNotFoundError):
            h = Hasher()
            h._source = nonexistentfile
            out = h._file_or_folder()

        with pytest.raises(FileNotFoundError):
            h = Hasher()
            h._source = nonexistentfolder
            out = h._file_or_folder()

    def test__normalise_source(self):

        validsource1 = Path(r"..\testdata\test1\subfolder1\testfile.txt")
        validoutput1 = Path('../testdata/test1/subfolder1/testfile.txt')

        validsource2 = r'   ..\testdata\test1\subfolder1\testfile.txt   '
        validoutput2 = Path('../testdata/test1/subfolder1/testfile.txt')

        validsource3 = r'   ../testdata/test1/subfolder1/testfile.txt   '
        validoutput3 = Path('../testdata/test1/subfolder1/testfile.txt')

        out = Hasher._normalise_source(validsource1)
        assert out == validoutput1

        out = Hasher._normalise_source(validsource2)
        assert out == validoutput2

        out = Hasher._normalise_source(validsource3)
        assert out == validoutput3

        # Test for home directory substitution, but only on Linux, or MacOS
        # This has not been tested on Macintosh, but I believe MacOS returns 'Darwin'
        this_os = platform.system().lower()
        if this_os == 'linux' or this_os == 'darwin':

            # Get the username to build the home directory string
            # If we are running as superuser, this will return `root` rather than the obvious username, so just exit
            username = getpass.getuser()
            assert username != 'root', "Test will fail if running as root, and test files are not in root's home folder"

            # Hoping `/home/username/Documents` is a valid location, otherwise we will get a FileNotFoundError
            source = Path("~/Documents")
            substituted_source = Path(f"/home/{username}/Documents")

            out = Hasher._normalise_source(source)
            assert out == substituted_source
