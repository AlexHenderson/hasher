# Hasher
# Copyright (c) 2022 Alex Henderson (alex.henderson@manchester.ac.uk)
# Licensed under the MIT License. See https://opensource.org/licenses/MIT
# SPDX-License-Identifier: MIT
# Version 1.1.0
# See https://github.com/AlexHenderson/hasher for the most recent version

import hashlib
import logging
from pathlib import Path
from typing import Union, AbstractSet


class Hasher:
    """
    Class to generate a stable hash value for either a single file, or a folder containing many files and sub-folders.

    Requires Python 3.7 or higher.

    Features:
    - The default hash type is 'sha256', although the user can specify any valid hash type provided by `hashlib`.
    - A single hash is generated from a folder, regardless of how many files and sub-folders it contains.
    - For a single file, the filename can be included into the hash if required (default is not to include).
    - Filenames relative to the initial source location are incorporated into the hash to define the folder structure.
    - For a folder, the folder name can be included into the hash if required (default is not to include).
    - Empty files and folders are hashed as their relative filename, thereby preserving the true folder structure.
    - Hashes of individual 'filename + file contents' hashes are first generated, before being sorted, and then
        re-hashed. This prevents issues with filename ordering during the recursion process.
    - The Posix version of folder names are used in the hash to allow for cross-platform stability.
    - Folder names are relative to the source location, not absolute paths. For example with a source location of
        'C:\mydata\hashme', with the following structure:

                C:\mydata\hashme
                C:\mydata\hashme\file1
                C:\mydata\hashme\file2
                C:\mydata\hashme\folder1\file3
                C:\mydata\hashme\folder1\subfolder2\file4

        The hash list will consist of individual hashes of:

            'hashme', (if requested; default is not to include)
            'hashme/file1' followed by the contents of that file,
            'hashme/file2' followed by the contents of that file,
            'hashme/folder1/file3' followed by the contents of that file,
            'hashme/folder1/subfolder2/file4' followed by the contents of that file.

        This hash list is then sorted for stability, before the final hash is calculated from each of the individual
        hashes.

        This process preserves the names, and relative locations, of each file within the folder structure, together
        with the contents of the files therein. Empty files and folders are also recognised by their filename.
    - Logging is implemented at the INFO level.

    Notes:
        Incorporation of the filename (single file hash), or folder name (folder hash), creates a hash that is a unique
        identifier of that file/folder, including its name. If the filename/folder name is not included (default), the
        hash will be a unique identifier for the *contents* of the file/folder, even if it has a different name.

        See `README.md` file for example usage.

    Copyright (c) 2022 Alex Henderson (alex.henderson@manchester.ac.uk)
    Licensed under the MIT License. See https://opensource.org/licenses/MIT
    SPDX-License-Identifier: MIT
    Version 1.1.0
    See https://github.com/AlexHenderson/hasher for the most recent version

    """

    # Define the version of this code
    _version = "1.1.0"

    # Define the default type of hash as 'sha256'
    _default_hash_type = 'sha256'

    @classmethod
    def version(cls) -> str:
        """
        Returns the version number of this code.

        :return: The version number.
        :rtype: str
        """

        return Hasher._version

    @classmethod
    def default_hash_type(cls) -> str:
        """
        Returns the default hash type.

        :return: The default hash type.
        :rtype: str
        """

        return Hasher._default_hash_type

    @classmethod
    def default_hash_name(cls) -> str:
        """
        Returns the default hash name.

        :return: The default hash name.
        :rtype: str
        """
        
        return Hasher._default_hash_type

    @classmethod
    def algorithms_guaranteed(cls) -> AbstractSet[str]:
        """
        Returns the list of hash types guaranteed to be supported on all platforms.

        :return: The default hash name.
        :rtype: AbstractSet[str]
        """
        
        return hashlib.algorithms_guaranteed

    @classmethod
    def _normalise_source(cls, source) -> Path:
        """
        Check the validity of the source input. If the input is a string, it is converted to a `pathlib.Path`.

        :param source: A file, or folder, from which to generate the hash.
        :type source: str, pathlib.Path
        :raises ValueError: Raised if `source` is neither a string, nor a pathlib.Path.
        :return: A `pathlib.Path` containing the source location.
        :rtype: pathlib.Path
        """
        
        if type(source) == str:
            temp = Path(source.strip())
        elif isinstance(source, Path):
            temp = source
        else:
            # The source is not a string or a Path, so abort
            raise ValueError('Location to hash must be a string or pathlib.Path')

        # If the source contains a home symbol (~) on Linux, expand that to an absolute path
        temp = temp.expanduser()

        return temp

    @classmethod
    def _normalise_hash_type(cls, hash_type) -> str:
        """
        Check the validity of the `hash_type` input.
        Only hashes that are guaranteed to be available across all platforms are allowed. See
        `hasher.algorithms_guaranteed()` for a list of these types.

        :param hash_type:
        :type hash_type:
        :raises ValueError: Raised if `hash_type` is not a string.
        :raises ValueError: Raised if `hash_type` is not amongst those guaranteed to be available across all platforms.
        :return: The `hash_type` provided.
        :rtype: str
        """
        
        if type(hash_type) != str:
            # The hash_type is not a string, so abort
            raise ValueError('Hash type must be a string')

        if hash_type not in hashlib.algorithms_available:
            raise ValueError(f"Hash type ('{hash_type}') not available. "
                             f"See hasher.algorithms_guaranteed() for a full list.")

        return hash_type

    def __init__(self):
        """
        Class constructor.
        `hash_type` is set to the `default_hash_type` value.
        """

        self._source = None
        self._hash_type = Hasher._default_hash_type
        self._hash = None
        self._include_source = False

    def generate(self,
                 source: Union[str, Path] = None,
                 hash_type: str = _default_hash_type,
                 include_source_str: bool = False):
        """
        Generate a hash of the file or folder provided in `source`.
        - If `source` is a filename this generates a hash of that file, prepended by its name if `include_source_str`
            is `True`
        - If `source` is a folder this recursively processes all files in the folder and generates a hash of the entire
            collection.
        The `hash_type` provides a mechanism to change the type of hash generated. The default is `'sha256'`.

        :param source: A file, or folder, from which to generate the hash.
        :type source: str, pathlib.Path
        :param hash_type: The type of hash to generate. Default is 'sha256'.
        :type hash_type: str, optional
        :param include_source_str: If `True` the name of the source file or folder is prepended to the hash.
            Default is `False`
        :type include_source_str: bool
        :return: The hash of the file or folder.
        :rtype: a hashlib object
        """

        logging.info(f"Hasher >>>>>>")

        # Log the version of this source code
        logging.info(f"Version: {Hasher._version}")

        try:
            # Normalise input
            self._source = self._normalise_source(source)
            self._hash_type = self._normalise_hash_type(hash_type)
            self._include_source = include_source_str

            logging.info(f"Type: {self._hash_type}")

            # Depending on whether `source` is a file or folder, follow the appropriate path
            source_type = self._file_or_folder()
            if source_type == 'file':
                logging.info(f"Source (file): {self._source}")
                self._file_hash()
            elif source_type == 'folder':
                logging.info(f"Source (folder): {self._source}")
                self._folder_hash()

            logging.info(f"Overall: {self._hash.hexdigest()}")

        except Exception as e:
            exception_type = type(e).__name__
            message = str(e)
            logging.error(f"{exception_type}: {message}")
            raise

        finally:
            logging.info(f"Hasher <<<<<<")

        return self._hash

    def source(self) -> Path:
        """
        Returns the hashed location (file name, or folder name) as a `pathlib.Path`.

        :return: The hashed location.
        :rtype: pathlib.Path
        """

        return self._source

    def hash_type(self) -> str:
        """
        Returns the type of hash used.

        :return: The type of hash used.
        :rtype: str
        """

        return self._hash_type

    def hash_name(self) -> str:
        """
        Returns the name of hash used.

        :return: The name of hash used.
        :rtype: str
        """

        return self._hash_type

    def hash(self):
        """
        Returns the generated hash object.

        :return: The generated hash.
        :rtype: a hashlib object
        """

        return self._hash

    def hexdigest(self) -> str:
        """
        Returns the generated hash value as a `hashlib.hexdigest` string.

        :return: The `hashlib.hexdigest` of the generated hash.
        :rtype: str
        """

        return self._hash.hexdigest()

    def _file_or_folder(self) -> str:
        """
        Determines whether the input refers to a file, or a folder.

        :raises ValueError: If `source` is other than a file or folder, for example a symbolic link.
        :raises FileNotFoundError: If `source` does not exist.
        :return: The type of input: 'file' or 'folder'.
        :rtype: str
        """

        source_type = None
        if self._source.exists():
            if self._source.is_file():
                source_type = 'file'
            elif self._source.is_dir():
                source_type = 'folder'
            else:
                raise ValueError("Sorry, we can only handle files and folders.")
        else:
            raise FileNotFoundError(f"Source ({self._source}) does not exist.")

        return source_type

    def _file_hash(self):
        """
        Generates a hash of a file, using the given `hash_type`.
        Here the Posix version of the filename (in UTF-8) is prepended to the file contents, if requested to do so.

        :return: The `hashlib.hexdigest` of the file.
        :rtype: str
        """

        self._hash = hashlib.new(self._hash_type)

        # Encode the filename as UTF-8 bytes and push into the hash generator, if requested to do so
        if self._include_source:
            self._hash.update(self._source.name.encode())

        # Extract the contents of the file as bytes, and push into the hash generator
        self._hash.update(self._source.read_bytes())

        logging.info(f"File: {self._source.name}, {self._hash.hexdigest()}")

    def _folder_hash(self):
        """
        Generates a hash generated from the folder, using the given `hash_type`.
        Here, a list of hashes is generated recursively from the folder. This includes:
            - the Posix version (in UTF-8) of the folder name, if requested to include the folder name
            - the Posix version (in UTF-8) of the relative location and filename of each file, with respect to the
              initial folder name, followed by the contents of that file.
        These hashes are then sorted, and a final hash is generated from the list.

        For example, if the folder `source` is `C:\mydata\hashme`, and the folder contents are:

            C:\mydata\hashme
            C:\mydata\hashme\file1
            C:\mydata\hashme\file2
            C:\mydata\hashme\folder1\file3
            C:\mydata\hashme\folder1\subfolder2\file4

        The hash list will consist of individual hashes of:

            'hashme', (only if requested this to be included: `include_source_str` == `True`)
            'hashme/file1' followed by the contents of that file,
            'hashme/file2' followed by the contents of that file,
            'hashme/folder1/file3' followed by the contents of that file,
            'hashme/folder1/subfolder2/file4' followed by the contents of that file.

        The list is then sorted for stability, before the final hash is calculated from each of the individual hashes.

        This process preserves the names, and relative locations, of each file and folder within the folder structure,
        together with the contents of the files therein. Empty files and folders are also recognised by their name.

        :return: The `hashlib.hexdigest` of the folder.
        :rtype: str
        """

        self._hash = hashlib.new(self._hash_type)

        # Encode the folder name as UTF-8 bytes and push into the hash generator, if requested to do so
        if self._include_source:
            self._hash.update(self._source.name.encode())
            logging.info(f"Folder: '{self._source.name}', {self._hash.hexdigest()}")
        else:
            logging.info(f"Folder: '{self._source.name}', (not included in hash)")

        # Collect a list of files in this folder and sub-folders
        folder_contents = list(self._source.rglob("*"))

        # Somewhere to hold the hash of each file/folder
        hash_digests = list()

        for entry in folder_contents:
            temp_hash = hashlib.new(self._hash_type)

            # Determine the relative location of this file or sub-folder, with respect to the source location
            relative_source = entry.relative_to(self._source)

            # Encode the relative file or folder name, as UTF-8 bytes and push into the hash generator
            temp_hash.update(relative_source.as_posix().encode())

            if entry.is_file():
                # Extract the contents of the file as bytes, and push into the hash generator
                temp_hash.update(entry.read_bytes())
                logging.info(f"File: '{relative_source.as_posix()}', {temp_hash.hexdigest()}")
            else:
                logging.info(f"Folder: '{relative_source.as_posix()}', {temp_hash.hexdigest()}")

            # Add this hash to the list of hashes
            hash_digests.append(temp_hash.hexdigest())

        # Take all the hashes produced from the files and the source folder name and sort into a reproducible order
        hash_digests.sort()

        # Take the sorted list of hashes and generate an overarching hash from that combination
        for digest in hash_digests:
            self._hash.update(digest.encode())
