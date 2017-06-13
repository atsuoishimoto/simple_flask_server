from setuptools import setup

setup(
    name = "simple_flask_server",
    version = "0.0.2",
    author = "Atsuo Ishimoto",
    author_email = "xatsuoi@gmail.com",
    description = "Flask equivalent of python -m SimpleHTTPServer.",
    license = "BSD",
    url = "https://github.com/atsuoishimoto/simple_flask_server",
    install_requires=[
        'flask',
        ],
    zip_safe=False,
    packages=['simple_flask_server'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ],
)
