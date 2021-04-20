from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="pike",
    version="0.0.0",
    url="https://github.com/RealOrangeOne/pike",
    author="Jake Howard",
    description="Like make, but Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="BSD",
    packages=find_packages(include="pike*"),
    package_data={"pike": ["py.typed"]},
    install_requires=[],
    project_urls={
        "Changelog": "https://github.com/RealOrangeOne/pike/releases",
        "Issues": "https://github.com/RealOrangeOne/pike/issues",
    },
    entry_points={"console_scripts": ["pike=pike.__main__:main"]},
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
)
