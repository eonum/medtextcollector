# TODO refactor - I don't like loading the __CONFIG__ global
from optparse import OptionParser
import json
import re

def load_config():
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="config", help="specify configuration file")
    parser.add_option("-d", "--debug",
                  action="store_true", dest="debug", default=False,
                  help="enable debug mode")
    (options, args) = parser.parse_args()

    if not options.config:
        options.config = 'configuration.json'
    
    config = Configuration(options.config, options.debug)
    return config

class Configuration(object):
    def __init__(self, config_path, debug):
        self.config = json.load(open(config_path, 'r'))
        self.config['config_path'] = config_path
        self.config['debug'] = debug
        self.obligatory_config_elements = [] # TODO extend
        self.validate_config()
        
    def validate_config(self):
        for config_element in self.obligatory_config_elements:
            if config_element not in self.config:
                raise ValueError(config_element + ' has to be present in configuration file.')
    
    def parse(self, e):
        if isinstance(e, str): 
            r = r'\$.*?\$'
            variables = re.findall(r, e)
            while len(variables) > 0:
                var = variables[0][1:-1]
                if isinstance(self.config[var], str):
                    e = e.replace('$'+var+'$', self.config[var])
                    variables = re.findall(r, e)
            return e
        
        elif isinstance(e, list):
            returned_list = []
            for s in e:
                s = self.parse(s)
                returned_list.append(s)
            return returned_list
        else:
            return e
    
    def __getattr__(self, attr):
        if not self.hasattr(attr) and attr in self.config:
            self.parse(self.config[attr])
        return self.__getattribute__(attr)
        
    def __getitem__(self, item):
        return self.parse(self.config[item])
        
__CONFIG__ = load_config()