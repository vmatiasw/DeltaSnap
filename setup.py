from setuptools import setup, find_packages

setup(
    name="DeltaDB",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    test_suite="tests",
    tests_require=[
        "pytest",
        "sqlalchemy",
    ],
    description="Librería para procesar y gestionar metadatos de bases de datos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Matias Viola",
    author_email="matiasvioladi@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
