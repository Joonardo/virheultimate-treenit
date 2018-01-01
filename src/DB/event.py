from DB import DB

users_in_table = DB.Table('users_in_table',
    DB.Column('user_id', DB.Integer, DB.ForeignKey('users.id'), primary_key=True),
    DB.Column('event_id', DB.Integer, DB.ForeignKey('events.id'), primary_key=True)
)

users_out_table = DB.Table('users_out_table',
    DB.Column('user_id', DB.Integer, DB.ForeignKey('users.id'), primary_key=True),
    DB.Column('event_id', DB.Integer, DB.ForeignKey('events.id'), primary_key=True)
)

class Event(DB.Model):
    __tablename__ = 'events'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80), nullable=False)
    description = DB.Column(DB.Text)
    users_in = DB.relationship('User', secondary=users_in_table,
                lazy='subquery', backref=DB.backref('events', lazy='joined'))
    users_out = DB.relationship('User', secondary=users_out_table, lazy='subquery')

    def __init__(self, n, desc):
        self.name = n
        self.description = desc
        self.users_in = []
        self.users_out = []

    def status_in(self, user):
        if user in self.users_out:
            self.users_out.remove(user)
        self.users_in.append(user)

    def status_out(self, user):
        if user in self.users_in:
            self.users_in.remove(user)
        self.users_out.append(user)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'users_in': [u.id for u in self.users_in],
            'users_out': [u.id for u in self.users_out],
        }
