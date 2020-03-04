import regex, os

from PyInquirer import Validator, ValidationError

def check_navigator(cmd):
    return {
        "back": "back" == ("back" if cmd in ["back","b"] else cmd), 
        "home": "home" == ("home" if cmd in ["home","h"] else cmd), 
        "exit": "exit" == ("exit" if cmd in ["exit","e"] else cmd), 
    }


class ModelPathValidator(Validator):
    def validate(self, path):
        ok = os.path.exists(path.text+"/__init__.py")
        if (not ok) | (sum(check_navigator(path.text).values()) > 0):
            raise ValidationError(
                message='Please enter a valid model path (model must be in __init__.py)',
                cursor_position=len(path.text))  # Move cursor to end

class PayloadPathValidator(Validator):
    def validate(self, path):
        ok = os.path.exists(path.text) & (path.text[-3:] in ["csv", "tsv"])
        if (not ok) | (sum(check_navigator(path.text).values()) > 0):
            raise ValidationError(
                message='Please enter a valid payload path (file must be csv or tsv)',
                cursor_position=len(path.text))  # Move cursor to end

class DeployPathValidator(Validator):
    def validate(self, path):
        ok = os.path.exists(path.text)
        if (not ok) | (sum(check_navigator(path.text).values()) > 0):
            raise ValidationError(
                message='Please enter a valid model path',
                cursor_position=len(path.text))  # Move cursor to end

class DummyValidator(Validator):
    def validate(self, name):
        if not len(name.text)>0:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(name.text))  # Move cursor to end

class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

class TagValidator(Validator):
    def validate(self, name):
        if not len(name.text)>0:
            raise ValidationError(
                message='Please enter a valid string',
                cursor_position=len(name.text))  # Move cursor to end