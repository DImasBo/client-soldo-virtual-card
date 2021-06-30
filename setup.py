from setuptools import setup, find_packages

setup(
    name='SoldoCard',
    version='0.0.1',
    url=' ',
    license='MIT',
    author='Dmytro Bondar',
    author_email='admin@affcountry.com',
    description='A small example package Notifier',
    long_description='file: README.md',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'sqlalchemy',
        'requests',
        'pydantic'
    ],
    tests_require=[
        'sqlalchemy',
        'requests',
        'pydantic'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='nose.collector'
)