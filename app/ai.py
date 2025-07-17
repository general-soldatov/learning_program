import random
from string import ascii_uppercase
from app.config import PROMPT, ROLE, THEMES, QUESTION, TEST
from app.parser import ProjectReader, ParseShedule

class AIPrompter:
    def __init__(self, data_yaml: ProjectReader, shedule: ParseShedule):
        self.name = shedule.name
        self.themes = data_yaml.themes.list_of
        self.division = data_yaml.themes.semester_division

    @staticmethod
    def themes_plan(themes: list, division: int):
        volume_last: list = []
        themes_ = [themes[:division], themes[division:]]
        volume_last.append({i+1: themes_[0][i] for i in range(division)})
        volume_last.append({i+1: themes_[1][i-division] for i in range(division, len(themes))})
        return volume_last

    def export_prompt(self):
        themes = self.themes_plan(self.themes, self.division)
        for elem in themes:
            text = PROMPT
            themes = '\n'.join((f"{key}. {value}" for key, value in elem.items()))
            text['messages'][0]['text'] = ROLE.format(name=self.name)
            text['messages'][1]['text'] = THEMES.format(themes=themes) + QUESTION
            print('Prompt to question\n', text)
            text['messages'][1]['text'] = THEMES.format(themes=themes) + TEST
            print('Prompt to test:\n', text)


class AITester:
    def __init__(self, data_yaml: ProjectReader):
        self.test = data_yaml._data['test']
        self.questions = data_yaml._data['questions']
        self.themes = len(data_yaml.themes.list_of)

    @staticmethod
    def create_test(test: dict) -> list:
        data = []
        for i, item in enumerate(test["test_tasks"], 1):
            text = item['question'] + '\n'
            text += '\n'.join((answer for answer in item['options']))
            data.append([i, text, item['answer']])
        return data

    @staticmethod
    def create_sequence(sequence: dict, num: int) -> list:
        text = sequence['task'] + '\n'
        numbers = list(range(1, len(sequence['steps']) + 1))
        random.shuffle(numbers)
        answers = {i: elem for elem, i in zip(sequence['steps'], numbers)}
        text += '\n'.join((f'{i}. {x}' for i, x in sorted(answers.items(), key=lambda a: a[0])))
        answer_true = ', '.join(map(str, numbers))
        return [num, text, answer_true]

    @staticmethod
    def create_comparison(comparison: dict, num: int) -> list:
        text = comparison['task'] + '\n'
        text += '\n'.join((f'{letter}. {elem}' for elem, letter in zip(comparison['terms'], ascii_uppercase)))
        numbers = list(range(1, len(comparison['definitions']) + 1))
        random.shuffle(numbers)
        answer_true = ', '.join([f'{letter}-{num}'
                                for letter, num in zip(ascii_uppercase, numbers)])
        answers = {i: elem for elem, i in zip(comparison['definitions'], numbers)}
        text += '\n\n'
        text += '\n'.join((f'{i}. {x}' for i, x in sorted(answers.items(), key=lambda a: a[0])))
        return [num, text, answer_true]

    def get_test(self, themes: int | str):
        test: dict = self.test[str(themes)]
        data = self.create_test(test)
        sequence = test.get("sequence_task", None)
        if sequence:
            data.append(self.create_sequence(sequence, data[-1][0] + 1))
        comparison = test.get("matching_task", None)
        if comparison:
            data.append(self.create_comparison(comparison, data[-1][0] + 1))
        return data

    def get_discussion(self, themes: int | str):
        questions = self.questions[str(themes)]
        return '\n'.join((f'{i}. {elem}'
                          for i, elem in enumerate(questions['discussions'], 1)))

    def get_question(self, themes: int | str):
        questions = self.questions[str(themes)]
        return '\n'.join((f'{i}. {elem}'
                          for i, elem in enumerate(questions['questions'], 1)))

    def build(self):
        return {
            str(item): {
                'question': self.get_question(item),
                'test': self.get_test(item),
                'discussion': self.get_discussion(item)
                } for item in range(1, self.themes)
            }
