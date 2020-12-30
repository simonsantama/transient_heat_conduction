import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="transient_heat_conduction",
    version="0.0.1",
    author="Simon Santamaria",
    author_email="simonsantama@gmail.com",
    description="Numerical implementation of direct and inverse heat diffusion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simonsantama/transient_heat_conduction",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows 10",
    ],
    python_requires='>=3.6',
)
