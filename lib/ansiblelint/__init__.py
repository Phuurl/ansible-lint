import ansiblelint.utils

class AnsibleLintRule(object):

    def __init__(self,
            id=None,
            description="",
            shortdesc="",
            tags=[]):
        self.id = id
        self.shortdesc = shortdesc
        self.description = description
        self.tags = tags

    def __repr__(self):
        return self.id + ": " + self.shortdesc

    def verbose(self):
        return self.id + ": " + self.shortdesc + "\n" + self.description


    def match(self, playbook=""):
        return []


class RulesCollection(object):

    def __init__(self):
        self.rules = []

    def register(self,obj):
        self.rules.append(obj)

    def __len__(self):
        return len(self.rules)

    def run(self, playbookfile, tags=None, skip_tags=None):
        text = ""
        matches = list()
        with open(playbookfile, 'r') as f:
            text = f.read()
        for rule in self.rules:
            if not tags or utils.tags_intersect(rule.tags, tags):
                if not skip_tags or not utils.tags_intersect(rule.tags, skip_tags):
                    matches.extend(Match.from_matches(playbookfile, rule, text))
        return matches

    def __repr__(self):
        return "\n".join([rule.verbose() for rule in sorted(self.rules, key = lambda x: x.id)])

    @classmethod
    def create_from_directory(cls, rulesdir):
        result = cls()
        result.rules = utils.load_plugins(rulesdir)
        return result


class Match:

    def __init__(self, linenumber, line, filename, rule):
        self.linenumber = linenumber
        self.line = line
        self.filename = filename
        self.rule = rule

    def __repr__(self):
        formatstr = "[{}] ({}) matched {}:{} {}"
        return formatstr.format(self.rule.id, self.rule.description,
                                self.filename, self.linenumber, self.line)

    @staticmethod
    def from_matches(filename, rule, text):
        lines = rule.match(text)
        results = [Match(line, text.split("\n")[line-1], filename, rule)
                for line in lines]
        return results