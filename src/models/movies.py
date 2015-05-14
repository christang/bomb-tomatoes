import re


class Movies(object):

    def __init__(self, movies):
        self.movies = movies
        self.movies_by_ID = {v.ID: k for k, v in enumerate(self.movies)}

        # define sets of existing movie types
        self.tags = reduce(lambda s, t: s | set(t), [m.tags for m in self.movies], set())
        self.decades = {m.year // 10 * 10 for m in self.movies}

    def __getitem__(self, item):
        try:
            movie_index = self.movies_by_ID[item]
            if self.movies[movie_index].ID == item:
                return self.movies[movie_index]
            else:
                raise
        except:
            raise Exception('unexpected movie index %d' % item)

    @staticmethod
    def parse_stream(stream):
        movies = [Movie.parse_entry(line) for line in stream]
        return Movies(movies)


class Movie(object):

    def __init__(self, id_, title, year, tags):
        self.ID = id_
        self.title = title
        self.year = year
        self.tags = tags

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
        index = int(items[0])
        title, year = Movie.parse_title_year(items[1])
        tags = items[2].split('|')
        return Movie(index, title, year, tags)

    @staticmethod
    def parse_title_year(item):
        match = re.match(r'^(.*)\((\d{4})\)$', item)
        if match:
            return match.group(1).strip(), int(match.group(2))
        else:
            raise Exception("couldn't parse " + item)

    def __repr__(self):
        return '::'.join([str(self.ID), self.title, str(self.year), '|'.join(self.tags)])
