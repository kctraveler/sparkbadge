from repository import Repository, repoFactory

class Metric:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository
        self.xvals = None
        self.yvals = None
        self.name = None
        

class Coverage(Metric):
    def __init__(self, repository: Repository) -> None:
        super().__init__(repository)
        #TODO Get coverage metrics from coveralls and set vals
        self.xvals = [90, 75, 90, 90 ] # remove later

class IssueDensity(Metric):
    def __init__(self, repository) -> None:
        super().__init__(repository)
        #TODO Get Issue Density
        self.xvals = [2, 4, 12, 15, 0]
        
