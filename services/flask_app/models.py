from app import db

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    group_size = db.Column(db.Integer)
    week_gap = db.Column(db.Integer)
    week_day = db.Column(db.String())
    time_of_day = db.Column(db.Time)
    
    def __init__(self, name, description, group_size, week_gap, week_day, time_of_day):
        self.id = name.replace(' ', '').lower()
        self.name = name
        self.description = description
        self.group_size = group_size
        self.week_gap = week_gap
        self.week_day = week_day
        self.time_of_day = time_of_day
    
    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'description': self.description,
            'group_size': self.group_size,
            'week_gap': self.week_gap,
            'week_day': self.week_day,
            'time_of_day': self.time_of_day,
        }
