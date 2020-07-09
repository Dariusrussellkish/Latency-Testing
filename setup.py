from setuptools import setup
from setuptools import find_packages

if __name__ == '__main__':
    setup(
        name='Latency-Testing',
        version=open('version.txt', 'r').read(),
        description='Test CloudLab TCP latencies',
        author='Darius Russell Kish',
        author_email='russeldk@bc.edu',
        packages=find_packages(),
        install_requires=[],
        setup_requires=["pytest-runner"],
        tests_require=["pytest"],
        include_package_data=True,
        zip_safe=False,
        scripts=[]
    )
