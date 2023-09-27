from abc import ABC, abstractmethod
from github import Github
import os
from dotenv import load_dotenv
import logging

class Repository(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.name_full = None
        self.owner = None
        self.name = None
    
    @abstractmethod
    def getCommits(self, lookback = 100):
        pass
    
    @abstractmethod
    def getIssues(self, lookback = 100):
        pass
  
class Commit(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.sha = None
             

class GHRepository(Repository):

    def __init__(self, name_full: str) -> None:
        super().__init__()
        self.name_full = name_full
        self.owner, self.name = self.name_full.split("/")
        self._repoapi = None
        
    def _setRepoApi(self) -> None: 
        try:
            load_dotenv()
            gh = Github(os.environ['GITHUB_TOKEN'], per_page=100)
            self.repoapi = gh.get_repo(self.name_full)
        except AttributeError as a:
            logging.warning("Github Token not found, unable to access GitHub API")
        except Exception as e:
            logging.warning(e)

        
    def getCommits(self, lookback = 100):
        if self._repoapi is None:
            self._setRepoApi()
        #TODO get commits from the repo API
        
    def getIssues(self, lookback = 100):
        if self._repoapi is None:
            self._setRepoApi()
        #TODO get issues list
        
def repoFactory(name_full: str, type = "GITHUB") -> Repository:
    if type == "GITHUB":
        return GHRepository(name_full)