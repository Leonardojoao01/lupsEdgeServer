# Em teste
from business_rules import run_all
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC, FIELD_TEXT
from ActionRules import ActionRules
from ConditionsRules import ConditionsRules
from Parameters import Parameters
import json
import os
#metodo que recebe o json que contem regras de contigencia
class EngineRule(object):
    """docstring for EngineRule"""


    def get_rules(self,a):

        rules = json.loads(a)
        return rules

    def get_parameters(self,obj_json):

        parameters = json.loads(obj_json)
        return parameters


    def run_rules(self,a,b):

        parameters = self.get_parameters(a) #
        obj_parameters= Parameters(parameters['evento'],parameters['id'],parameters['valor'])
        rules = self.get_rules(b)

        run_all(rule_list=rules,
                defined_variables=ConditionsRules(100),
                defined_actions=ActionRules(obj_parameters),
                stop_on_first_trigger=True
            )
    def run_rules(self,a):

        parameters = self.get_parameters(a) #
        obj_parameters= Parameters(parameters['evento'],parameters['id'],parameters['valor'])
        rules = self.get_rules(parameters['id'])

        run_all(rule_list=rules,
                defined_variables=ConditionsRules(100),
                defined_actions=ActionRules(obj_parameters),
                stop_on_first_trigger=True
            )
