from setuptools import setup, find_packages

__version__ = '1.0.0'

setup(name='snacky',
      version=__version__,
      description='',
      author='Hans Daigle',
      author_email='hansdaigle@me.com',
      url='https://github.com/HansDaigle/snacky',
      packages=find_packages(),
      install_requires=["fastapi", "uvicorn[standard]", "gunicorn"],
      )
