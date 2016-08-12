from GetValuesSensor import *
from moduleOfRules.EngineRuleEdge import EngineRule
import json

class Gathering(object):

    def set_id(self, id_sensor):
        self.id_sensor = id_sensor

    def get_id(self):
        return self.id_sensor

    def set_val_sensor(self, vsensor):
        self.vsensor = vsensor

    def get_val_sensor(self):
        return self.vsensor

    def regra(self,id_sensor,valor,id_gateway,contador):   # Verificar argumentos e criar objeto p chamar regras
        engine = EngineRule()

        string_rule = '{{ "evento": "e", "id": {0},"valor": {1}, "id_gateway": {2}, "contador": {3} }}'.format(id_sensor,valor,id_gateway,contador)
        #engine.run_rules(string_rule)

        print('ENTROU NA REGRA')

    def processamento(self,id_sensor,select_features): # 0 = OBJECT or 1 = FUNCTION
                                # Cria um objeto COMMUNICATION, que retorna um valor do sensor
                                # Realiza um if, verificando se precisa criar um  REGRA ou apenas
                                # retorna um dado
        #valor_sensor =
        colecter_sensor = GetValuesSensor()
        formation = colecter_sensor.get_values_on_gatway()            # <--------- Passar argumentos
        #self.set_val_sensor(valor_sensor);
        #print(type(formation))
        #formation = json.loads(formation)

        id_g = formation['id_gateway']
        id_s = formation['id_sensor']
        value = formation['value']
        contador = formation['contador']

        print(value)


        if select_features == 0:              # Chama a REGRA
            self.regra(id_s,value,id_g,contador)
            print("REGRA 0")

        else :                  # Retorna o valor do sensor
            #return self.get_val_sensor();
            self.regra(id_s,value,id_g,contador)
            print("REGRA 1")
            #iasdhajkhsdjhad