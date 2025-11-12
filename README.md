### Run these commands

`Clear any __pycache__ folder if it ends up on your machine`

- If you see a .env file put the required credentials there, if for some reasons, .env is not there, go to the next step  else skip it 
- Make a .env file with the contents of .env.sample
- Put the required values

### Run this command to load the table schemas on your machine
```
mysql -u root -p college < ./create.sql
```

#### If you are on linux run these commands 
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app main run
```

#### If you are on windows run these in powershell 
```
python3 -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate
pip install -r requirements.txt
flask --app run
```
