# Joomla Packager

A command line utility for packaging Joomla! extensions for release.

## Getting Started

```
git clone https://github.com/codewiseio/joomla-packager.git
virtualenv -p python3 venv
pip install -r requirements.txt
```


### Prerequisites

Python 3


## usage


Collect files from Joomla installation folder to source
```
jpack.py -c;
```

Package extension for distribution
```
jpack.py -p;
```

Collect and package files
```
jpack.py -cp;
```

Perform operation in different directory
```
jpack.py --source=path/to/extension/source -c;
```

## Authors

* **Jeffrey Hallock** <codewiseio@gmail.com>

## License

(c) 2018 Jeffrey Hallock, Codewise Software

This project is licensed under the MIT License.
