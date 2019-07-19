from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='kiwizen',
    version='0.0.2',
    description= 'Funny and useful codes',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Zen Shawn',
    author_email='xiaozisheng2008@qq.com',
    maintainer='Zen Shawn',
    maintainer_email='xiaozisheng2008@qq.com',
    license='BSD License',
    #packages=find_packages(),
    packages=['kiwizen.plt', 'kiwizen.alg'],
    platforms=["all"],
    url='https://github.com/xiaodaxia-2008/Kiwi',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'scipy', 'matplotlib']
)
