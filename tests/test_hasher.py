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

        # Empty folders are not version controlled by Git. Therefore, we create a folder structure to test the ability
        # of this package to create a hash of an empty folder.

        # Create folder structure and add a file to it
        folder = Path(r"..\testdata\folder\subfolder")
        folder.mkdir(parents=True, exist_ok=True)

        # Add a file with contents
        file = Path(folder / "testfile.txt")
        with file.open(mode="wt") as f:
            f.write("Some text in a file.")
            f.write("Another line of text.")

        # Create an empty folder
        empty_folder = Path(r"..\testdata\folder\emptysubfolder")
        empty_folder.mkdir(parents=True, exist_ok=True)

        # Create an empty file
        empty_file = Path(folder / "empty_file.txt")
        empty_file.touch()

        # Define a file and a folder that do not actually exist
        nonexistent_file = Path(r"..\testdata\folder\subfolder\blahblah.txt")
        nonexistent_folder = Path(r"..\testdata\folder\blahblah")

        # Test a folder is identified as a 'folder'
        h = Hasher()
        h._source = folder
        out = h._file_or_folder()
        assert out == 'folder'

        # Test a file is identified as a 'file'
        h = Hasher()
        h._source = file
        out = h._file_or_folder()
        assert out == 'file'

        # Test an empty folder is identified as a 'folder'
        h = Hasher()
        h._source = empty_folder
        out = h._file_or_folder()
        assert out == 'folder'

        # Test an empty file is identified as a 'file'
        h = Hasher()
        h._source = empty_file
        out = h._file_or_folder()
        assert out == 'file'

        # Test we throw an exception when a file does not exist
        with pytest.raises(FileNotFoundError):
            h = Hasher()
            h._source = nonexistent_file
            out = h._file_or_folder()

        # Test we throw an exception when a folder does not exist
        with pytest.raises(FileNotFoundError):
            h = Hasher()
            h._source = nonexistent_folder
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
