from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='enfusion_api',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.0',
        'pandas>=1.0',
    ],
    author='Henry Whelan',
    author_email='henrywhelan93@gmail.com',
    description='A package to interact with Enfusion API and retrieve data as pandas DataFrames.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/h1whelan/enfusion_api',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)