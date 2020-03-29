from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='idb',
    version='1.0.0',
    description='Build an image dataset with your webcam',
    py_modules=["DatasetBuilder"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Sakir Ozturk',
    author_email='ozturk213@hotmail.fr',
    install_requires=[
        'opencv-python>= 4.2.0'
    ],
    url="https://github.com/YnsOzt"
)