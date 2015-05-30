from zip_code import ZipCode


Ages = {
    1:  "Under 18",
    18:  "18-24",
    25:  "25-34",
    35:  "35-44",
    45:  "45-49",
    50:  "50-55",
    56:  "56+"
}


Occupations = [
    "other",                 # 0
    "academic/educator",     # 1
    "artist",                # 2
    "clerical/admin",        # 3
    "college/grad student",  # 4
    "customer service",      # 5
    "doctor/health care",    # 6
    "executive/managerial",  # 7
    "farmer",                # 8
    "homemaker",             # 9
    "K-12 student",          # 10
    "lawyer",                # 11
    "programmer",            # 12
    "retired",               # 13
    "sales/marketing",       # 14
    "scientist",             # 15
    "self-employed",         # 16
    "technician/engineer",   # 17
    "tradesman/craftsman",   # 18
    "unemployed",            # 19
    "writer"                 # 20
]


class Users(object):

    def __init__(self, users):
        self.users = users

        # define sets of existing user types
        self.genders = {True, False}
        self.occupations = {u.occupation for u in self.users}
        self.age_groups = {u.age_group for u in self.users}
        self.zip_codes = {u.zip_code for u in self.users}

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

    def __init__(self, id_, is_male, age_group, occupation, zip_code, detailed_geo=True):
        self.ID = id_
        self.is_male = is_male
        self.age_group = age_group
        self.occupation = occupation
        self.zip_code = ZipCode(zip_code) if detailed_geo else zip_code

        self.r_ids = None
        self.count = None
        self.amean = None
        self.hmean = None
        self.var = None

    def summarize(self, r_ids, count, amean, hmean, var):
        self.r_ids = r_ids
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
