import shelve
import yaml

from jinja2 import Environment, FileSystemLoader
from pymongo import MongoClient

from eveweasel import paster

CONFIG = 'eveweasel.yml'

class EveWeasel(object):
    def __init__(self):
        with open(CONFIG) as conf_file:
            conf_data = conf_file.read()
        self.config = yaml.load(conf_data)
        self.jinja = Environment(loader=FileSystemLoader('eveweasel/templates/'))
        self.mongo = MongoClient()
        self.db = self.mongo.eveweasel
        
    def get_paths(self):
        return (paster.PATHS)

