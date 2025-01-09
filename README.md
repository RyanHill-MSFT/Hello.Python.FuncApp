# Local Setup

From the [app directory](./app/) run the following:

```bash
python -m venv .venv # Create virtual environment
. .\venv\Scripts\Activate.ps1 # Activate virtual environment
python -m pip install --upgrade pip # Upgrade pip
pip install -r requirements.txt # Install dependencies
```

# Changes 1

* (lightly) update [pyproject.toml](./modules/subspace/pyproject.toml)
* Remove [setup.py](./modules/subspace/setup.py)
* Add dependency on [subspace module](./modules/subspace/) to [requirements.txt](./app/requirements.txt)
* Remove arcgis from [requirements.txt](./app/requirements.txt)
  * There seemed to be some unrelated error when installing this package

# Changes 2

* Change [communication.py](./modules/subspace/src/communication.py) to [subspace.py](./modules/subspace/src/subspace.py)
  * See https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#src-layout-vs-flat-layout