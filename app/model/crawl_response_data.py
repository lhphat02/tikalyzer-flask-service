class CrawlResponseData:
    def __init__(self, file = "", path = "", elapsed_time = 0, row_count = 0):
        self.file = file
        self.path = path
        self.elapsed_time = elapsed_time
        self.row_count = row_count

    def to_dict(self):
        return {
            'file': self.file,
            'path': self.path,
            'elapsed_time': self.elapsed_time,
            'row_count': self.row_count
        }