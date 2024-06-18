# The `analytic_tools` module

To install this package run

```
python3 -m pip install . in the code directory
```

To make this package editable (development mode) run in the same location:

```
pip install --editable .
```

Whenever you need a module from the package, write for instance:

```python
from analytic_tools import utilities

```

To check if the package has been installed correctly, run:

```
python3 test/test_utilities.py
```

which imports the `utilities` module from `analytic_tools`.
