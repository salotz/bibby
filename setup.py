from setuptools import setup, find_packages

setup(
    name='bibby',
    version='0.1',
    author="Samuel D. Lotz",
    author_email="samuel.lotz@salotz.info",
    description="Small python library and CLI for doing stuff with Bibsonomy",
    py_modules=['bibby'],
    url="https://github.com/salotz/bibby",
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
