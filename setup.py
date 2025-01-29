from setuptools import setup, find_packages

setup(
    name="deltasnap",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    extras_require={
        "django": ["Django>=3.0"],
        "sqlalchemy": ["SQLAlchemy>=1.3"],
        "all": [
            "Django>=3.0",
            "SQLAlchemy>=1.3",
        ],
    },
    test_suite="tests",
    tests_require=["pytest"],
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
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    keywords="metadata management, database, SQLAlchemy, Django, functional testing, debugging, ORM, database capture, data analysis, data comparison, database records, test automation, test framework, database testing, software testing",
)
