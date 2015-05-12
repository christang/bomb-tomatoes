Occupations = [
    "other",
    "academic/educator",
    "artist",
    "clerical/admin",
    "college/grad student",
    "customer service",
    "doctor/health care",
    "executive/managerial",
    "farmer",
    "homemaker",
    "K-12 student",
    "lawyer",
    "programmer",
    "retired",
    "sales/marketing",
    "scientist",
    "self-employed",
    "technician/engineer",
    "tradesman/craftsman",
    "unemployed",
    "writer"
]


class Users(object):

    def __init__(self, users):
        self.users = users

    def __getitem__(self, item):
        try:
            user = self.users[item-1]
            if user.ID == item:
                return user
            else:
                raise
        except:
            raise Exception('unexpected user index %d' % item)

    @staticmethod
    def parse_stream(stream):
        users = [User.parse_entry(line) for line in stream]
        return Users(users)


class User(object):

    def __init__(self, id_, is_male, age_group, occupation, zip_code):
        self.ID = id_
        self.is_male = is_male
        self.age_group = age_group
        self.occupation = occupation
        self.zip_code = zip_code

        self.count = None
        self.amean = None
        self.hmean = None
        self.var = None

    def summarize(self, ratings, count, amean, hmean, var):
        self.count = count
        self.amean = amean
        self.hmean = hmean
        self.var = var

    @staticmethod
    def parse_entry(line):
        items = line.strip().split('::')
        return User(int(items[0]), items[1] == 'M', int(items[2]), int(items[3]), items[4])

    def __repr__(self):
        gender = 'M' if self.is_male else 'F'
        return '::'.join([str(self.ID), gender, str(self.age_group),
                          Occupations[self.occupation], self.zip_code])
