Python-Couchdbhelper
==============

Kudos to [RockYou](http://www.rockyou.com) for supporting open source!

## Overview

    ch = CouchHelper('http://localhost:5984')
    ch.select("example")
    ch.save({'test': 'data'})

    # This will save any file here to couchdb's design docs.
    ch.sync_view('/path/to/app/views/')

