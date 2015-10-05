from sphinx.domains.std import StandardDomain


def setup(app):
    StandardDomain.initial_data['labels']['routingtable'] = (
        'http-routingtable',
        '',
        'HTTP Routing Table')
    StandardDomain.initial_data['anonlabels']['routingtable'] = (
        'http-routingtable',
        '')