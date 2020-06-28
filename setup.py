import setuptools

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

setuptools.setup(
    name="django_celery_progressbar",
    version="0.1.1",
    author="Eugene Prodan",
    author_email="mora9715@gmail.com",
    description="Progress bar for Django Celery application",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    url="https://github.com/mora9715/django-celery-progressbar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers"

    ],
    python_requires='>=3.6',
    install_requires=[
        'django',
        'celery'
    ]
)