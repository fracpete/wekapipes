from setuptools import setup, find_namespace_packages


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="wekapipes",
    description="Allows defining and running of Weka pipelines for data conversion, filtering, and modeling.",
    long_description=(
            _read('DESCRIPTION.rst') + b'\n' +
            _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/fracpete/wekapipes",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    license='MIT License',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    install_requires=[
        "setuptools",
        "seppl>=0.2.21",
        "kasperl>=0.0.1",
        "wai_logging",
        "python_weka_wrapper3",
    ],
    version="0.0.1",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    entry_points={
        "console_scripts": [
            "wp-run=wp.tool.convert:sys_main",
            "wp-exec=wp.tool.exec:sys_main",
            "wp-find=wp.tool.find:sys_main",
            "wp-help=wp.tool.help:sys_main",
            "wp-registry=wp.registry:sys_main",
            "wp-test-generator=wp.tool.test_generator:sys_main",
        ],
        "class_lister": [
            "wp=wp.class_lister",
        ],
    },
)
