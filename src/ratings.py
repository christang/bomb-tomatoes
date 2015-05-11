

class Ratings(object):

    def __init__(self, ratings):
        self.ratings = ratings

    def for_movie(self, id_):
        return [r for r in self.ratings if r.m_id == id_]

    def for_user(self, id_):
        return [r for r in self.ratings if r.u_id == id_]

    @staticmethod
    def parse_stream(stream):
        ratings = [Rating.parse_entry(line) for line in stream]
        return Ratings(ratings)


class Rating(object):

    def __init__(self, u_id, m_id, rating, timestamp):
        self.u_id = u_id
        self.m_id = m_id
        self.rating = rating
        self.timestamp = timestamp

    @staticmethod
    def parse_entry(line):
        items = line.split('::')
        return Rating(int(items[0]), int(items[1]), int(items[2]), items[3])

    def __repr__(self):
        return '::'.join([str(self.u_id), str(self.m_id), str(self.rating), self.timestamp])