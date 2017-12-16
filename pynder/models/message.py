# encoding=utf8

import dateutil.parser
from six import text_type

def quote_str(string):
    return '%' + string + '%'


class Message(object):

    def __init__(self, data, user=None):
        self._data = data
        self.sent = dateutil.parser.parse(data['sent_date'])
        self.body = data['message']
        if user:
            if data['from'] == user.id:
                self.sender = user
            if data['to'] == user.id:
                self.to = user
            if data['from'] == user._session.profile.id:
                self.sender = user._session.profile
            if data['to'] == user._session.profile.id:
                self.to = user._session.profile

    def __unicode__(self):
        return self.body

    def __str__(self):
        return text_type(self).encode("utf8")

    def __repr__(self):
        return repr(self.body)

    @property
    def csv_header(self):
        return ','.join([
            'sent', 'body',
            'from', 'to'
        ])

    def to_csv(self):
        return ','.join(str(f) for f in [
            self.sent.isoformat(),
            quote_str(
                unicode(self.body)
                .encode('utf-8')
                .replace('\n', '')
                .replace(',', '')
                .replace('%', '')),
            self.sender.id,
            self.to.id
        ])
