import os
import setuptools


setuptools.setup(
    name="dyco",
    description="a silly discord bot",
    url="https://github.com/phagara/dyco",
    version=os.environ.get("DYCO_VERSION"),
    license="BSD 2-Clause License",
    platforms=["any"],
    entry_points={"console_scripts": ["dyco=dyco.__main__:main"]},
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "discord.py",
        "PyYAML",
        "urlextract",
        "humanize",
        "transliterate",
        "tabulate",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.9",
        "Environment :: No Input/Output (Daemon)",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
    ],
)
