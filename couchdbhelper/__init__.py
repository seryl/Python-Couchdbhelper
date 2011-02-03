import couchdb
from couchdb.design import ViewDefinition

import json
import os

class CouchHelper(object):
    def __init__(self, server, database=None):
        self.couch = None
        self.db = None
        self.server = server
        self.database = database
        self.is_connected = False
        self.connect()

    def connect(self):
        self.couch = couchdb.Server(self.server)
        if self.database:
            self.select(self.database)

    def disconnect(self):
        self.db = None
        self.is_connected = False

    def select(self, database):
        if not database:
            raise Exception("No database selected")
        try:
            self.db = self.couch[database]
            self.is_connected = True
        except:
            try:
                self.couch.create(database)
                self.db = self.couch[database]
                self.database = database
                self.is_connected = True
            except:
                self.database = None
                self.db = None
                self.is_connected = False

    def save(self, data):
        """Save a document or list of documents"""
        if not self.is_connected:
            raise Exception("No database selected")
        if not data:
            return False
        if isinstance(data, dict):
            doc = couchdb.Document()
            doc.update(data)
            self.db.create(doc)
        elif isinstance(data, couchdb.Document):
            self.db.update(data)
        elif isinstance(data, list):
            self.db.update(data)
        return True

    def get_view(self, name, view):
        if not self.is_connected:
            raise Exception("No database selected")
        return self.db.view('_design/%s/_view/%s' % (name, view))

    def sync_view(self, f, remove_missing=False):
        def get_file(filename):
            viewlist = []
            data = open(filename).read()
            data = json.loads(data)

            if data['_id'].startswith('_design/'):
                design = data['_id'][8:] # removing _design/
            else:
                design = data['_id']
            language = data['language']
            for k,v in data['views'].iteritems():
                name = k
                map_func = v['map']
                if v.has_key('reduce'):
                    reduce_func = v['reduce']
                else:
                    reduce_func = None
                view = ViewDefinition(
                    design, name, map_func, reduce_func, language)
                viewlist.append(view)

            return viewlist

        def get_directory(path):
            viewlist = []
            for f in os.listdir(path):
                current = os.path.join(path, f)
                viewlist = list(set.union(set(viewlist), set(get_file(current))))
            return viewlist

        if not self.is_connected:
            raise Exception('Error: Not connected to a database!')

        if os.path.isfile(f):
            viewlist = get_file(f)
        elif os.path.isdir(f):
            viewlist = get_directory(f)

        return ViewDefinition.sync_many(
            self.db, viewlist, remove_missing=remove_missing)


