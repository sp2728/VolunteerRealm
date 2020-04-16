from VolunteerRealm.app import create_app, db, setup_database

app= create_app();
db.init_app(app)
setup_database(app)