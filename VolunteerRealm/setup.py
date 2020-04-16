from VolunteerRealm.app import create_app, db

app= create_app();
db.init_app(app)