# EarDVFS: Environment-Adaptable RL-based DVFS for Mobile Devices



[<img src="https://img.shields.io/badge/license-MIT-blue">](https://github.com/vwxyzjn/cleanrl)


EarDVFS is a Environment-adaptable RL-based DVFS for mobile devices.

We implemented this project by referring to the following excellent open-source projects.
We sincerely thank their contributors:

* [CleanRL](https://github.com/vwxyzjn/cleanrl)
* [zTT](https://github.com/ztt-21/zTT)
* [gearDVFS](https://github.com/geardvfs/GearDVFS)


## Get started

Prerequisites:
* Python >=3.7.1,<3.11
* [Poetry 1.2.1+](https://python-poetry.org)

To run experiments locally, give the following a try:

```bash
git clone https://github.com/vwxyzjn/cleanrl.git && cd cleanrl
poetry install

# alternatively, you could use `poetry shell` and do
# `python run DVFS/defaultDVFS.py`
poetry run python DVFS/defaultDVFS.py
```

If you are not using `poetry`, you can install CleanRL with `requirements.txt`:

```bash
# core dependencies
pip install -r requirements/requirements.txt
```

To run DVFS:

```
./run.sh
```

The commands in the `run.sh` file will be helpful for running the DVFS.

