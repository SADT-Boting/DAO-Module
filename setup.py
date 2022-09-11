import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="DAO-module",
    version="1.0",
    author="BuldakovN",
    author_email="nikitabuldakov@mail.ru",
    description="Модуль для работы с удаленной БД",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SADT-Boting/DAO-Module",
    packages=['DAO'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=["pymysql"]
)