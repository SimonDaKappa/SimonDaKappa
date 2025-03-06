import requests
import pathlib
import datetime
import math

from typing import List

root = pathlib.Path(__file__).parent.resolve()


class XPHolder:

    def __init__(self, xps, new_xps):
        self.xps = xps
        self.new_xps = new_xps
    
    def __lt__(self, value):
        return self.xps < value.xps
    
    def __le__(self, value):
        return self.xps <= value.xps
    
    def __gt__(self, value):
        return self.xps > value.xps
    
    def __ge__(self, value):
        return self.xps >= value.xps

class Machine(XPHolder):

    def __init__(self, name, xps, new_xps):
        super().__init__(xps, new_xps)
        self.name = name
    
    def __str__(self):
        return f"<Machine {self.name} with {self.xps} XP>"

class Language(XPHolder):

    def __init__(self, name, xps, new_xps):
        super().__init__(xps, new_xps)
        self.name = name
    
    def __str__(self):
        return f"<Language {self.name} with {self.xps} XP>"

class Date:

    def __init__(self, date, xp):
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.xp = xp
    
    def __str__(self):
        return f"<Date {self.date} with {self.xp} XP>"

class User:

    def __init__(self, user, total_xp, new_xp, machines, languages, dates):
        self.user = user
        self.total_xp = total_xp
        self.new_xp = new_xp

        self.machines = sorted([
            Machine(k, v['xps'], v['new_xps']) for k, v in machines.items()
        ], key=lambda item: item.xps, reverse=True)
        self.languages = sorted([
            Language(k, v['xps'], v['new_xps']) for k, v in languages.items()
        ], key=lambda item: item.xps, reverse=True)
        self.dates = sorted([Date(k, v) for k, v in dates.items()], key=lambda item: item.xp, reverse=True)
    
    def __str__(self):
        return f"<User {self.user} with {self.total_xp} XP>"

def get_levels():
    levels_response = requests.get("https://codestats.net/api/users/SimonDaKappa").json()
    me = User(levels_response['user'], levels_response['total_xp'], levels_response['new_xp'], levels_response['machines'], levels_response['languages'], levels_response['dates'])
    return me

def to_level(xp):
    LEVEL_FACTOR = 0.025
    return int(math.floor(LEVEL_FACTOR * math.sqrt(xp)))

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'k', 'M', 'B', 'T', 'P'][magnitude])

def generate_language_line(language: Language):
    line = f"| {language.name} | {to_level(language.xps)} | {human_format(language.xps)} | {human_format(language.new_xps)} |"
    return line

def generate_md_table(languages: List[Language]):
    header = """| Language | Level | Total XP | XP gained (last 12 hours) |\n| --- | --- | --- | --- |"""
    body = "\n".join(list(map(generate_language_line, languages)))
    return f"""{header}
{body}"""

if __name__ == "__main__":
    readme_path = root / "README.MD";

    exp_total = get_levels()
    lang_top_ten = exp_total.languages[:10]
    md_table = generate_md_table(lang_top_ten)

    readme = f"""
[![wakatime](https://wakatime.com/badge/user/50e6c678-94a9-4739-af51-360aeb113c51.svg)](https://wakatime.com/@50e6c678-94a9-4739-af51-360aeb113c51)

- 👋 Hi, I’m @SimonDaKappa
- 🧑‍💼 I currently work at Emerson!
- 👀 I’m interested in Optimization, Full Stack Development, Reinforcement Learning, Machine Learning, Embedded Software, and whatever the breeze brings.
- 🌱 I graduated with a B.S. Dual in Computer Science and Mathematics, with a focus in Operations Research and A.I

My **Current Projects** 
- A full-stack rewrite of NeRF-Or-Nothing; A micro-service Deep Learning powered 3D video reconstruction application.
- A full-stack RAG Chatbot, with Knowledge Graph / Embedding Community Optimization, and CI/CD pipeline integration.
  - (This one is private, sorry)
I've been coding for 4 years, trying to expose myself to as many technologies as possible. I've recently started to track all my progress, so see
a list with my most used languages below!

{md_table}"""

    with open(readme_path, 'w') as f:
        f.write(readme)
