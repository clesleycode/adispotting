""" controls the details of ADI spotting"""

class ADISpotting:
    def __init__(self):
        self.winner = "U56FWRC3D"
        self.users = {}

    def add_user(self, user):
        self.users[user] = 0

    def add_points(self, user, points):
        self.users[user] = self.users[user] + points
        if self.users[self.winner] < self.users[user]:
            self.winner = user
    
    def get_points(self, user):
        return(self.users[user])