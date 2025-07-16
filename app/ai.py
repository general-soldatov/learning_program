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
