from distutils.core import setup

setup(name='Distutils',
      version='1.0',
      description='Interesting things',
      author='Zen Shawn',
      author_email='xiaozisheng2008@qq.com',
      download_url='https://github.com/xiaodaxia-2008/Kiwi',
      packages=['kiwi', 'kiwi.plt'],
      install_requires=["scipy", "numpy", "matplotlib"]
      )
