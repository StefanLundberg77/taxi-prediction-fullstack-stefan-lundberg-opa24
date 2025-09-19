from setuptools import setup
from setuptools import find_packages

# find_packages will find all the packages with __init__.py
print(find_packages())

# uv pip install -e . (if uv)
setup(
    name="taxipred",
    version="0.0.1",
    description="this package contains taxipred app",
    author="Stefan Lundberg",
    author_email="bjorn.stefan.lundberg@gmail.com",
    install_requires=["streamlit", "pandas", "fastapi", "uvicorn", "ipykernel", "matplotlib", "seaborn"],
    package_dir={"": "src"},
    package_data={"taxipred": ["data/*.csv"]},
    packages=find_packages(),
)
