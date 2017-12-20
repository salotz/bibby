from setuptools import setup, find_packages

setup(
    name='bibby',
    version='0.1',
    py_modules=['bibby'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Bibsonomy',
        'Pybtex'
    ],
    entry_points={
        'console_scripts' : [
            "bibby = bibby.cli:cli"]}

)
