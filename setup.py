import setuptools

import slacktokens

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name='slacktokens',
    version=slacktokens.__version__,
    url="https://github.com/hraftery/slacktokens",
    author="Heath Raftery",
    author_email="heath@empirical.ee",

    py_modules=['slacktokens'],
    python_requires=">=3.7",
    
    description="Extract personal tokens and authentication cookie from the Slack app.",
    long_description=readme,
    long_description_content_type="text/markdown",

    install_requires=[
      'leveldb',
      #'pycookiecheat',
      # Turns out "direct links" are forbidden by PyPi. Could use "requirements.txt" and
      # some instructions...  Ref: https://stackoverflow.com/q/68073819/3697870
      #'pycookiecheat@git+https://github.com/hraftery/pycookiecheat.git@a82d32730b01ebe20393ab5ca7b3267975ed0767#egg=pycookiecheat'
      'pycookiecheat-slack'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
