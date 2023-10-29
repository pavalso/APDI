from setuptools import setup, find_packages


setup(
    name="apdi-blobs",
    version="1.0.0",
    description="APDI Blobs Server",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "blob_server=blobsapdi.server:main"
        ]
    }
)
