import os
import json
from StaticEplusEngine import run_eplus_model, convert_json_idf


# EnergyPlus simulation which support two parameters setting , getting and execulate simulation
class EnergyPlusSimulation(object):
    # construction function
    def __init__(self):
        self.first_key = []
        self.first_val = []
        self.second_key = []
        self.second_val = []

    # set the first key
    def set_first_key(self, key):
        self.first_key = key

    # get the first key
    def get_first_key(self):
        return self.first_key

    # set the second key
    def set_second_key(self, key):
        self.second_key = key

    # get the second key
    def get_second_key(self):
        return self.first_key

    # set the first val
    def set_first_val(self, val):
        self.first_val = val

    # get the first val
    def get_first_val(self):
        return self.first_val

    # set the second val
    def set_second_val(self, val):
        self.second_val = val

    # get the second val
    def get_second_val(self):
        return self.first_val

    def run_two_simulation_helper(self, eplus_run_path, idf_path, output_dir,
                                  parameter_key1, parameter_val1,
                                  parameter_key2, parameter_val2):
        """
    	This is a helper function to run one simulation with the changed
    	value of the parameter_key
    	"""
        ######### step 1: convert an IDF file into JSON file #########
        convert_json_idf(eplus_run_path, idf_path)
        epjson_path = idf_path.split('.idf')[0] + '.epJSON'

        ######### step 2: load the JSON file into a JSON dict #########
        with open(epjson_path) as epJSON:
            epjson_dict = json.load(epJSON)

        ######### step 3: change the JSON dict value #########
        inner_dict = epjson_dict
        for i in range(len(parameter_key1)):
            if i < len(parameter_key1) - 1:
                inner_dict = inner_dict[parameter_key1[i]]

        inner_dict[parameter_key1[-1]] = parameter_val1
        inner_dict[parameter_key2[-1]] = parameter_val2

        ######### step 4: dump the JSON dict to JSON file #########
        with open(epjson_path, 'w') as epjson:
            json.dump(epjson_dict, epjson)

        ######### step 5: convert JSON file to IDF file #########
        convert_json_idf(eplus_run_path, epjson_path)

        ######### step 6: run simulation #########
        run_eplus_model(eplus_run_path, idf_path, output_dir)
        return output_dir + '/eplusout.csv'


    def simulation(self, eplus_run_path, idf_path, output_dir):
        res_dict = {}
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        for parameter_val1 in self.first_val:
            for parameter_val2 in self.second_val:
                sub_path = str(parameter_val1) + '_' + str(parameter_val2)
                this_output_dir = output_dir + f'/{sub_path}'
                this_res_path = self.run_two_simulation_helper(eplus_run_path,
                                                          idf_path,
                                                          this_output_dir,
                                                          self.first_key,
                                                          parameter_val1,
                                                          self.second_key,
                                                          parameter_val2)
                res_dict[sub_path] = this_res_path

        return res_dict
