import setuptools

import slacktokens

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setuptools.setup(
    name='slacktokens',
    version=slacktokens.__version__,
    url="https://github.com/hraftery/slacktokens",
    author="Heath Raftery",
    author_email="heath@empirical.ee",

    py_modules=['slacktokens'],
    python_requires=">=3.7"
    license='GPLv3',
    
    description="Extract personal tokens and authentication cookie from the Slack app.",
    long_description=readme,
    long_description_content_type="text/markdown",

    install_requires=[
      'leveldb',
      #'pycookiecheat',
      'git+https://github.com/hraftery/pycookiecheat@a82d32730b01ebe20393ab5ca7b3267975ed0767#egg=pycookiecheat'
    ],
)
