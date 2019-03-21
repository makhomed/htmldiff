from setuptools import setup, find_packages

setup(
    name="htmldiff",
    version="1.0.0.dev7",
    author="Ian Bicking - https://github.com/ianb",
    description=("Tool for diffing html files"),
    license='MIT',
    packages=find_packages('src'),
    package_dir={"": "src"},
    install_requires=["boltons>=17.1.0"],
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "htmldiff = htmldiff.entry_point:main",
        ]
    }
)
