import json

class Response:
    
    def __init__(self, input:json):
        self.__input = input
        self.__status = "In progress"
        
        
    def set_status(self, new_status:str):
        self.__status = new_status
    
    
    def set_status_code(self, status_code:int):
        '''
        Dos status code:
        0: Todo OK
        1: Error en la peticion o interno
        '''
        self.__status_code = status_code
    
            
    def set_response(self, response):
        self.__response =  response
    
        
    def jsonify(self):
        #obtengo el diccionario de atributos del objeto y luego lo jsonifico
        return json.dumps({
            'input':self.__input,
            'status_code':self.__status_code,
            'status':self.__status,
            'response':self.__response
        }) 
    
        
        
    
    