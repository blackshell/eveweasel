from datetime import datetime
from hashlib import sha1
from jinja2 import Template
from random import randint
from tornado.web import RequestHandler, HTTPError

MIN_POST_ID = 16**4
MAX_POST_ID = 16**6

class NewPasteHandler(RequestHandler):
    def get(self):
        template_args = {}
        template = self.application.weasel.jinja.get_template('new_paste.html')
        output = template.render(template_args)
        self.write(output)

    def post(self):
        db = self.application.weasel.db

        newpost_id = None
        
        text = self.get_argument("text")
        digest = sha1(str(text).encode()).hexdigest()
        if db.paster.find({'prehash': digest}).count():
            # If it already exists, no need to duplicate
            newpost_id = db.paster.find_one({'prehash': digest})['id']
        
        if not newpost_id:
            paste_obj = {}
            paste_obj['text'] = text
            paste_obj['date'] = datetime.utcnow()
            paste_id = hex(randint(MIN_POST_ID, MAX_POST_ID))[2:]
            while db.paster.find({'id': paste_id}).count():
                paste_id = hex(randint(MIN_POST_ID, MAX_POST_ID))[2:]
            paste_obj['id'] = paste_id
            paste_obj['prehash'] = digest
                
            db.paster.save(paste_obj)
            newpost_id = paste_id
        
        self.redirect('/p/%s' % newpost_id)

class ViewPasteHandler(RequestHandler):
    def get(self, paste_id):
        template_args = {}
        db = self.application.weasel.db
        
        paste_obj = db.paster.find_one({'id': paste_id})
        if not paste_obj:
            raise HTTPError(404)
        template_args['paste'] = paste_obj

        template = self.application.weasel.jinja.get_template('view_paste.html')
        output = template.render(template_args)
        self.write(output)


PATHS = [ ("/p/new", NewPasteHandler),
          ("/p/(.*)", ViewPasteHandler),
          ]

