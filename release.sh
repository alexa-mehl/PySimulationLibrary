rm -rf dist
python3.5 setup.py sdist
twine upload dist/*
