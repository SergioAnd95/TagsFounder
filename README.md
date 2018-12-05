## TagsFounder
#### Task:
Create service(REST API), that get text and return list of founded tags

#### Setup project local:
1. `git clone https://github.com/SergioAnd95/sturdy-tribble.git`
2. `cd TagsFounder`
3. `pip3 install -r requirements.txt` or `pip install -r requirements.txt` if you use virtualenv
4. Create file .env in settings directory(what content must be in .env file you can see in .env.example)
5. Setup your database in .env file(item #4) and run `alembic upgrade head` (for create all tables in your db)
6. If have error(ModuleNotFoundError) in migration so make `export PYTHONPATH=/path/to/your/project`
7. For start project run command `python app.py` or `python3 app.py`
