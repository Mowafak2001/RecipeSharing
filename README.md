Activate Virtual Environment
CREATE NEW VENV FOR EACH SESSION. UPDATE requirements.txt IF YOU ADD NEW PACKAGES
venv is in .gitignore so it should not be in the repository. we keep an updated list of dependencies in requirements.txt.
mac
python3 -m venv venv
windows
python -m venv venv

mac
source venv/bin/activate
windows
bin/Scripts/Activate

Install requirments.txt
pip install -r requirements.txt

UPDATE requirements.txt
pip freeze > requirements.txt
