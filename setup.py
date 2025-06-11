from setuptools import setup, find_packages

setup(
    name="markdown-typst",
    version="0.1.4",
    author="eWloYW8",
    author_email="3171132517@qq.com",
    description="A Markdown extension to compile typst code blocks to SVG.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eWloYW8/markdown-typst",
    packages=find_packages(),
    install_requires=[
        "markdown",
        "typst",
    ],
    entry_points={
        "markdown.extensions": [
            "typst = markdown_typst.typst_extension:TypstExtension",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires='>=3.6',
)
