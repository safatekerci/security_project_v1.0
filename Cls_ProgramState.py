from pymongo import MongoClient

class Cls_ProgramState(object):

    def __init__(self):
        self.client = MongoClient()
        self.connSecurity = self.client.ConnectionSecurityDB

    #Control program state and allows program to terminate
    def fnc_control_program_state(self):
        programState = ([z['program_state'] for z in list(self.connSecurity.ProgramStateColl.find({'id': 1}))])
        if (str(programState).replace('[', '').replace(']', '') == '1'):
            return True
        else:
            return False

    #Change state to terminate program
    def fnc_terminate_program(self):
        self.connSecurity.ProgramStateColl.update(
          {'id': 1},
          {
           '$set': {'program_state': 1}
          })
    #Change state to terminate program
    def fnc_start_program(self):
        self.connSecurity.ProgramStateColl.delete_many({})
        self.connSecurity.ProgramStateColl.insert_one(
            {
              'id': 1,
              'program_state': 0
            })








