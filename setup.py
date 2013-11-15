from distutils.core import setup

setup(
    name='MPIScope',
    version='0.1.0',
    author='David E. Shere',
    author_email='david.e.shere@gmail.com',
    packages=['mpiscope'],
    scripts=['bin/run.sh', 'bin/example.py'],
    #url=[''],
    license="LICENSE.txt",
    description='Provides a context for MPI based graphics programs.',
    long_desciption=open('README.txt').read(),
    install_requires=[
        "mpi4py"
    ],
)

