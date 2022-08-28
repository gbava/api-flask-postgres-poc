import os
import pandas as pd
from flask.cli import FlaskGroup
from src.app import create_app, db

csv_file_path = 'titanic.csv'
my_env = os.getenv('FLASK_ENV')
app = create_app(my_env)
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()
        db.session.commit()

@cli.command('seed_db')
def seed_db():
    engine = db.get_engine()
    print("seeding db...")
    # Read CSV with Pandas
    with open(csv_file_path, 'r') as file:
        df = pd.read_csv(file)
        # Insert to DB
        df.to_sql('people', con=engine, if_exists='replace')


if __name__ == '__main__':
    cli()
