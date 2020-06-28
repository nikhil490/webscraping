import os
import doi
from flask import (Flask, render_template, request, url_for,
                   redirect, flash, current_app)
from werkzeug.utils import secure_filename
from flask_classful import FlaskView, route
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import database
import export
import scrape
import api


app = Flask(__name__)
app.config.from_object(Config)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass
try:
    os.makedirs(app.config['UPLOAD_FOLDER'])
except OSError:
    pass

out_db = {'book': [],
          'article': [],
          'paper': [],
          }
doi_s = ''

api.ApiView.register(app, route_base='/api/')


class DOIView(FlaskView):
    """
            **Create application**
            This creates an instance of the flask app and runs it
    """

    route_base = '/'
    excluded_methods = ['allowed_file', 'upload_contents']

    @route('/')
    def index(self):
        return render_template("search/search_doi.html")

    @route('/', methods=['POST'])
    def search_doi(self):
        global out_db, doi_s
        list_doi = []
        if request.method == 'POST':
            if 'doi' in request.form:
                list_doi = request.form['doi'].split(',')
            if 'file' in request.files:
                file = request.files['file']
                if file and self.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    extension = file.filename.rsplit('.', 1)[1].lower()
                    path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(path)
                    list_doi = self.upload_contents(extension, path)
                else:
                    flash('Please upload only csv and json formats')
            list_doi = list(dict.fromkeys(list_doi))
            doi_s = list_doi
            domain = {}
            for i in list_doi:
                try:
                    doi.validate_doi(i)
                    domain[i] = doi.get_real_url_from_doi(i)
                except ValueError:
                    flash(f'{i} : is not valid , please try again')
                    doi_s.remove(i)
            if doi_s is None:
                return redirect(url_for('DOIView:index'))
            doi_temp = database.check(doi_s)
            if doi_temp:
                doi_ = doi_temp
                domains = [domain[i] for i in doi_ if i in domain]
                doi_temp.clear()
                scrap = scrape.Scrape()
                success = scrap.scrape(domains, app.config['DICT_OF_SPIDERS'])
                if success:
                    for i in success:
                        print('i in succscc', i)
            out_db = database.read(doi_s)
        return render_template("search/search_doi.html", context=out_db)

    @route('/download/<int:file_bool>', methods=['GET', 'POST'])
    def download(self, file_bool):
        global out_db
        temp_name, mimetype = export.export(out_db, file_bool)
        path = os.path.join(current_app.root_path, temp_name)

        def generate():
            with open(path) as f:
                yield from f
            os.remove(path)

        r = current_app.response_class(generate(), mimetype=mimetype)
        r.headers.set('Content-Disposition', 'attachment', filename=temp_name)
        return r

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

    def upload_contents(self, extension, path):
        import json
        import csv
        path = path
        if extension == 'csv':
            with open(path, newline='') as file:
                content = csv.reader(file, quotechar='|')
                list_of_doi = [j for i in content for j in i]
                while "" in list_of_doi:
                    list_of_doi.remove("")
        else:
            with open(path, 'r') as json_file:
                content = json.load(json_file)
                list_of_doi = [i for k, v in content.items() for i in v]
        return list_of_doi


DOIView.register(app)
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
