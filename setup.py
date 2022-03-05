from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hasher-AlexHenderson",
    version="1.1.0",
    author="Alex Henderson",
    author_email="alex.henderson@manchester.ac.uk",
    description="Python package to generate a stable hash value for either a single file, or a folder containing many "
                "files and sub-folders.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexHenderson/hasher",
    project_urls={
        "Bug Tracker": "https://github.com/AlexHenderson/hasher/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)
