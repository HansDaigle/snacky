from distutils.core import setup

__version__ = '1.0.0'

setup(name='snacky',
      version=__version__,
      description='',
      author='Hans Daigle',
      author_email='hansdaigle@me.com',
      url='https://github.com/HansDaigle/snacky',
      packages=['snacky'],
      install_requires=["fastapi", "uvicorn[standard]", "gunicorn"],
      )
