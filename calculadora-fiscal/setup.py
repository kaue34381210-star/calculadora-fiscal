from setuptools import setup, find_packages

setup(
    name="calculadora-fiscal",
    version="1.0.0",
    description="Calculadora de impostos para operações empresariais (CLI)",
    author="Seu Nome",
    python_requires=">=3.8",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "calculadora-fiscal=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
