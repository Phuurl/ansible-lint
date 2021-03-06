# Copyright (c) 2016, Will Thames and contributors
# Copyright (c) 2018, Ansible Project

from ansiblelint import AnsibleLintRule


class LineTooLongRule(AnsibleLintRule):
    id = '204'
    shortdesc = 'Lines should be no longer than 120 chars'
    description = (
        'Long lines make code harder to read and '
        'code review more difficult'
    )
    tags = ['formatting']
    version_added = 'v4.0.0'

    def match(self, file, line):
        return len(line) > 120
