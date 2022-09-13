import setuptools

setuptools.setup(
    name="DAO_module",
    version="1.2.1.1",
    author="BuldakovN",
    author_email="nikitabuldakov@mail.ru",
    description="Модуль для работы с удаленной БД",
    url="https://github.com/SADT-Boting/DAO-Module",
    packages=['dao_module'],
    python_requires='>=3.5',
    install_requires = [
        "PyMySQL >= 1.0",
        "pymysql >= 1.0"
    ],
)