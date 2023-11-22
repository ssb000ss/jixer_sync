from setuptools import setup, find_packages

setup(
    name='jixer-sync',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='ssb000ss',
    author_email='ssb000ss@gmail.com',
    description='A Python library for using Search engines.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ssb000ss/jixer-sync',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
