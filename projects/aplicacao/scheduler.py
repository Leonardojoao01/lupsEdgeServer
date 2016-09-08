from datetime import datetime
import json
import time
import re
import os
import threading
import pycurl
from array import array
from io import BytesIO
from event_treatment import *
from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerEdge(object):

    sensor_ant = []
    sensor_add = []

    def __init__(self):             #instância do objeto e inicia o escalonador

        def run_thread():
            while(True):
                time.sleep(1)

        self.scheduler = BackgroundScheduler()          # atribui um agendador background
        self.scheduler.start()                          # inicia o agendador
        self.th = threading.Thread(target= run_thread)  # thread executa outtro fluxo para o agendador rodar
        self.th.start()

    def add_job(self, a): # cria uma nova tarefa no escalonador
        jsonObject = json.loads(a)

        if(jsonObject['modo']=='cron'):
            self.scheduler.add_job(self.function, jsonObject['modo'], second = jsonObject['info']['second'], minute = jsonObject['info']['minute'],
            hour = jsonObject['info']['hour'], day = jsonObject['info']['day'], month = jsonObject['info']['month'], year = jsonObject['info']['year'],id = jsonObject['id_sensor'], args = [a])

    def remove_job(self, id_tarefa):    # id_tarefa - É ID do sensor a ser removido
        teste = str(id_tarefa)
        self.scheduler.remove_job(teste)

    def function(self,response):    # response - É JSON passado como argumento
        jsonObject = json.loads(response)
        object_events = Event_Treatment()
        object_events.event(1,response)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def start_process(self):
        sensors_data = self.check_sensor()
        scheduler_data = self.check_schedules()

        sensors_actual = []

        for sensor in sensors_data:
            id_sensor = sensor['id']
            sensors_actual.append(sensor)

        self.compara_DB(sensors_actual)         # Repassa um JSON com todos os dados de sensores cadastrados "NOVOS"

        aux_sensor_add = self.sensor_add
        if len(aux_sensor_add) != 0:            # Por algum motivo não funciona colocando direto o "self.sensor_add"
                                                            #                oO
            self.activa_scheduler(scheduler_data)     # Repassa os dados e cria objeto scheduler para adicionar no CRON as tarefas

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


    def check_sensor(self):
        #-------------------Usado para pegar dados em formato JSON----------------------
        headers = {'Authorization':'token %s' % "878559b6d7baf6fcede17397fc390c5b9d7cbb77"}
        url = 'http://localhost:8000/sensors/?format=json'
        request = requests.get(url, headers=headers)
        jsonObject = request.json()
        #-------------------------------------------------------------------------------
        return jsonObject

    def check_schedules(self):
        #-------------------Usado para pegar dados em formato JSON----------------------
        headers = {'Authorization':'token %s' % "878559b6d7baf6fcede17397fc390c5b9d7cbb77"}
        url = 'http://localhost:8000/schedules/?format=json'
        request = requests.get(url, headers=headers)
        jsonObject = request.json()
        #-------------------------------------------------------------------------------
        return jsonObject

    def compara_DB(self, dados):
        global sensor_ant
        global sensor_add
        sensor_remove = []
        add = 0
        not_existe = 1
        existe = 0
        teste = self.sensor_ant

        if len(teste) == 0:         # Quando nenhuma JOB está no CRON
            for row in dados:
                add = add +1
                self.sensor_ant.append(row)
                self.sensor_add.append(row)

        else:                       # Quando já possui JOBs no CRON
            # sensor_add -> Sensores que serão add no CRON, após add a tab fica vazia
            # sensor_ant -> Sensores que estão rodando no CRON
            # dados -> Sensores que estão no DB
            #-------------------Deleta os sensores na tabela antiga-----------------
            for sens in self.sensor_ant:
                for row in dados:
                    if sens['id'] == row['id']:
                        not_existe = 0
                if not_existe == 1:    # remover em relação ao ID, pois é único
                    print("Removeu JOB: ", sens['id'])
                    self.remove_job(sens['id'])   #   <------------------------------------------------------
                    sensor_remove.append(sens)

                not_existe = 1
        #-----------------------------------------------------------------------
            ##---------REMOVE SENSORES DA TABELA ANTIGA-------------------------
            for sens_r in sensor_remove:
                self.sensor_ant.remove(sens_r)
            sensor_remove.clear()
            #-------------------------------------------------------------------


        #-------------Adiciona sensores não cadastrados no CRON-----------------
            for row in dados:
                for sens in self.sensor_ant:
                    if row['id'] == sens['id']:
                        existe = 1

                if existe == 0:
                    self.sensor_ant.append(row)
                    self.sensor_add.append(row)
                existe = 0
        #-----------------------------------------------------------------------

    def activa_scheduler(self, dados_scheduler):
        #global asd
        global sensor_add

        for sens in self.sensor_add:
            json_new = self.create_JSON(sens,dados_scheduler) # Mescla os sensores no DB com dados do scheduler da API
            self.add_job(json_new)

        self.sensor_add.clear()


    def create_JSON(self, sensor,dados_sched):  # Cria um JSON no formato exato que SCHEDULER
                                    # irá utilizar. QQ tratamento deve ocorrer aqui.
        job = {}
        info = {}
        for row in dados_sched:
            if row['sensor'] == sensor['id']:

                job['modo'] = "cron"
                job['id_sensor'] = str(sensor['id'])
                job['event'] = "gathering"
                job['gateway'] = sensor['gateway']

                info['second'] = "*/{}".format(row['minute'])
                info['minute']  = "*"
                info['hour'] = "*"
                info['day'] = "*"
                info['week'] = "*"
                info['month'] = "*"
                info['year'] = "*"

                job['info'] = info
                #print(job)
        return json.dumps(job)
#-------------------------------------------------------------------------------
