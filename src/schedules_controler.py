from response import Response
import constants
import json
import traceback
from itertools import combinations
from flask import Flask, request



app = Flask(__name__)


'''
Llamar a endpoint de Django desde Flask

@app.route('/postjango')
def post_to_django():
    input = request.get_json()
    response = requests.post("horarios.com/getmihorario",json=input)
'''

@app.route('/getcombinations', methods=['POST'])
def return_combinations() -> json:
    input = request.get_json()
    response = Response(input=input)
    try:
        schedules = validate_json(
            json_schedule = input
        )
        valid_schedule = validate_schedule(gen_combinations(schedules))
        if valid_schedule:
            response.set_status(constants.OK_MESSAGE)
            response.set_status_code(constants.STATUS_CODE_OK)
            response.set_response(valid_schedule)
        else:
            raise ValueError('No valid schedules where found')
    except Exception as error:
        response.set_status(f"{constants.ERROR_MESSAGE}\nError: {traceback.format_exc()}")
        response.set_status_code(
            status_code= constants.STATUS_CODE_ERROR
        )
        response.set_response(None)
    finally:
        return response.jsonify()

        
def validate_json(json_schedule:json) -> list:
    try:
        schedules = json_schedule['schedule']
        if not isinstance(schedules, list):
            raise ValueError("Schedule must be type list")
        if len(schedules) < constants.MINIMUM_SUBJECTS:
            raise ValueError("There has to be more than 2 subjects to compute")
        return [tuple(schedule) for schedule in schedules] #convertir una matriz a una lista de tuplas
    except Exception as error:
        raise ValueError(f"{constants.ERROR_MESSAGE} in validate json module\nError: {error}")
    


def gen_combinations(schedules:list) -> list:
    schedule_combinations = []
    
    for r in range(constants.MINIMUM_SUBJECTS, constants.MAXIMUM_SUBJECTS):
        schedule_combinations.extend(list(combinations(schedules, r))) #+=
    return schedule_combinations



def validate_schedule(schedules_combinations:list) -> None:
    horarios_validos = []
    for combinacion in schedules_combinations:
        horarios_usados = set()
        nombres_clases = set()
        valido = True
        for horario in combinacion:
            dia1 = horario[1]
            dia2 = horario[2]
            hora_inicio1 = horario[3]
            hora_inicio2 = horario[5]
            nombre_clase = horario[0]
            
            if ((dia1, hora_inicio1) in horarios_usados or
                (dia2, hora_inicio2) in horarios_usados or
                nombre_clase in nombres_clases):
                valido = False
                break
            
            horarios_usados.add((dia1, hora_inicio1))
            horarios_usados.add((dia2, hora_inicio2))
            nombres_clases.add(nombre_clase)
        
        if valido:
            horarios_validos.append(combinacion)
    return horarios_validos


if __name__ == '__main__':
    app.run(debug=True)