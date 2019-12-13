import datetime as dt

UINT64 = 8
UINT32 = 4
CHAR = 1
DOUBLE = 8
FLOAT = 4
CHUNK = 1000000

class User:
    def __init__(self, user_id, username, birth_timestamp, gender):
        self.user_id = user_id
        self.username = username
        self.birth_date = dt.datetime.fromtimestamp(birth_timestamp)
        self.gender = gender

    def __str__(self):
        fbirth_date = self.birth_date.strftime('%B %d, %Y')
        if self.gender == 'f':
            fgender = 'female'
        elif self.gender == 'm':
            fgender = 'male'
        else:
            fgender = 'other'
        return f'user {self.user_id}: {self.username}, ' \
               f'born {fbirth_date} ({fgender})'

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id and \
            self.username == other.username and \
            self.birth_date == other.birth_date and \
            self.gender == other.gender

    def __len__(self):
        return UINT64 + UINT32 + len(self.username) + UINT32 + CHAR