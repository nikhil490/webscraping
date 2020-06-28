from flask import (request, url_for, current_app,
                   redirect, jsonify)
from flask_classful import FlaskView, route
import database
import doi
import scrape

out_db = {'book': [],
          'article': [],
          'paper': [],
          }
doi_s = ''


class ApiView(FlaskView):
    """
            **Create application**
            This creates an instance of the DOIApi and runs it
    """

    def index(self):
        if 'doi' in request.args:
            global doi_s
            doi_s = str(request.args['doi'])
        else:
            return 'Error:'
        global out_db
        if doi_s == 'all':
            out_db = database.read_all()
            return redirect(url_for('ApiView:display_all'))
        try:
            doi.validate_doi(doi_s)
            domain = doi.get_real_url_from_doi(doi_s)
        except ValueError:
            return 'Invalid doi'
        doi_temp = database.check([doi_s])
        if doi_temp:
            scrap = scrape.Scrape()
            scrap.scrape([domain], current_app.config['DICT_OF_SPIDERS'])
        out_db = database.read([doi_s])
        return redirect(url_for('ApiView:display_all'))

    @route('/display_all')
    def display_all(self):
        global out_db
        data_ = [k for i, j in out_db.items() if j for k in j]
        return jsonify(data_)
