# Hasher #

Python package to generate a stable hash value for either a single file, or a folder containing many files and 
sub-folders.

## Features ##
- The default hash type is `sha256`, although the user can specify any valid hash type provided by `hashlib`.
- A single hash is generated from a folder, regardless of how many files and sub-folders it contains.
- For a single file, the filename can be included into the hash if required (default is not to include).
- Filenames relative to the initial source location are incorporated into the hash to define the folder structure.
- For a folder, the folder name can be included into the hash if required (default is not to include).
- Empty files and folders are hashed as their relative filename, thereby preserving the true folder structure.
- Hashes of individual 'filename + file contents' hashes are first generated, before being sorted, and then
    re-hashed. This prevents issues with filename ordering during the recursion process.
- The Posix version of folder names are used in the hash to allow for cross-platform stability.
- Folder names are relative to the source location, not absolute paths. For example with a source location of
    `C:\mydata\hashme`, with the following structure:

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
    with the contents of the files therein. Empty files and folders are also recognised by their filename/folder name
- Logging is implemented at the INFO level.

## Notes ##
Incorporation of the filename (single file hash), or folder name (folder hash), creates a hash that is a unique
identifier of that file/folder, including its name. If the filename/folder name is not included (default), the
hash will be a unique identifier for the *contents* of the file/folder, even if it has a different name.

## Examples ##

### Example 1 ###
Assuming a folder with a source location of `C:\mydata\hashme`, generate a hash of the folder and contents 
using `sha256`, and excluding the folder name (`hashme`). The `hexdigest` here is an example output.     

    from hasher import Hasher

    source = r"C:\mydata\hashme"
    hasher = Hasher()
    h = hasher.generate(source)
    if h:
        print(f"source: {source}")
        print(f"hash name: {h.name}")
        print(f"hash digest: {h.hexdigest()}")
        print("...or...")
        print(f"source: {hasher.source()}")
        print(f"hash name: {hasher.hash_name()}")
        print(f"hash digest: {h.hexdigest()}")

output  

    source: C:\mydata\hashme
    hash name: sha256
    hash digest: 71d7434...<snip>...8077fb
    ...or...
    source: C:\mydata\hashme
    hash name: sha256
    hash digest: 71d7434...<snip>...8077fb

### Example 2 ###
Scenario as for Example 1. Generate a `md5` hash

    from hasher import Hasher

    source = r"C:\mydata\hashme"
    hasher = Hasher()
    h = hasher.generate(source, hash_type='md5')
    if h:
        print(f"hash name: {h.name}")
        print(f"hash digest: {h.hexdigest()}")

output

    hash name: md5
    hash digest: 64be08f...<snip>...924872

### Example 3 ###
Scenario as for Example 2, but incorporating the folder name in the hash.

    from hasher import Hasher

    source = r"C:\mydata\hashme"
    hasher = Hasher()
    h = hasher.generate(source, hash_type='md5', include_source_str=True)
    if h:
        print(f"hash name: {h.name}")
        print(f"hash digest: {h.hexdigest()}")

output

    hash name: md5
    hash digest: f2865fa...<snip>...6679c3

## Requirements ##

    python >= 3.7
    pytest

### Installation ###

    pip install hasher-AlexHenderson==1.1.1


## Usage rights ##
Copyright (c) 2022 Alex Henderson (alex.henderson@manchester.ac.uk)   
Licensed under the MIT License. See https://opensource.org/licenses/MIT      
SPDX-License-Identifier: MIT   
Version 1.1.1   
See https://github.com/AlexHenderson/hasher for the most recent version  
