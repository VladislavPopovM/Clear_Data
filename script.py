from jsonschema.validators import Draft7Validator
import json, os
from jsonschema import ErrorTree, validate

#CONST
ROOT_DIR = os.getcwd()
way_schema = ROOT_DIR + '/schema/'
way_data = ROOT_DIR + '/event/'
list_files_data = os.listdir(way_data)
list_way_schema = os.listdir(way_schema)
ARR_ERRORS = []

def spawn_log(text):
    with open('Errors.log', 'w') as f:
        for Error in  ARR_ERRORS:
            if Error == '!':
                Error = '\n'
            if Error in 'Error(s)':
                f.write('\n' + Error)
            f.write(Error + '\n')

def main(list_files):
    for i in range(len(list_files)):
        with open(way_data + list_files[i], 'r') as rf:
            data = json.load(rf)
        try:
            event = data['event']
            try:
                with open(way_schema + event + '.schema', 'r') as rf:
                    schema = json.load(rf)
                validator = Draft7Validator(schema = schema)
                errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
                if len(errors) != 0:
                    ARR_ERRORS.append(f'Error(s) in file {list_files[i]}')
                for error in errors:
                    ARR_ERRORS.append(f'{error.message}')
                ARR_ERRORS.append(f'!')
            except FileNotFoundError:
                 ARR_ERRORS.append(f'Error in file {list_files[i]}: FileNotFoundError')
        except TypeError:
            ARR_ERRORS.append(f'Error in file {list_files[i]}: name is wrong')
        except KeyError:
            ARR_ERRORS.append(f'Error in file {list_files[i]}: event not found')

main(list_files_data)
spawn_log(ARR_ERRORS)