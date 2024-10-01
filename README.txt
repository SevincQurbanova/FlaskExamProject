py -m pip --version
py -m pip install pip //1-ce defe

py -m venv venv
venv/Scripts/activate
pip install -r requirements.txt

docker-compose up -d
docker-compose down

flask db init
flask db migrate -m "Initial migration"
flask db upgrade



Terminalda flask shell  yazdiqda 

$env:FLASK_APP="app:create_app"
echo$FLASK_APP# or $env:FLASK_APP in PowerShell

exit() yazdiqda flaskin shellinden cixir Terminala qayidir


http://127.0.0.1:5000/
http://127.0.0.1:5000/admin

py app.py   proyekti run edir,
ctrl+C dayandirir

