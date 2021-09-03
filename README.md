# Data analysis
- Document here the project: gdelt
- Description: Google BigQuery Pipelines with Python
- Data Source: https://console.cloud.google.com/bigquery?project=gdelt-bq&page=table&t=events&d=gdeltv2&p=gdelt-bq&redirect_from_classic=true


Data extracted from https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for gdelt in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/gdelt`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "gdelt"
git remote add origin git@github.com:{group}/gdelt.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
gdelt-run
```

# Install

Go to `https://github.com/{group}/gdelt` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/gdelt.git
cd gdelt
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
gdelt-run
```