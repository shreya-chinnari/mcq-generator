from setuptools import setup, find_packages

setup(
    name="mcq_generator",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai",
        "langchain",
        "streamlit",
        "python-dotenv",
        "pypdf2"
    ],
    author="Shreya Chinnari",
    author_email="shreya16180@gmail.com"
)
