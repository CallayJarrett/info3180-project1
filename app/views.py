"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
import locale
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app.forms import PropertyForm 
from app.models import Property
from werkzeug.utils import secure_filename
locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Callay Jarrett")

@app.route('/properties')
def properties():
    """Render the website's properties page."""
    properties = Property.query.all()

    return render_template('properties.html', propertylist = properties, loc =locale)

@app.route('/properties/create', methods=['POST','GET'])
def create_properties():
    """Render the Flask-WTF to add new property page"""
    form = PropertyForm()

    if request.method == 'GET':
        return render_template('create_properties.html', form=form)
    
    if request.method == 'POST':
         if form.validate_on_submit:
             file = request.files['photo']
             secured = secure_filename(file.filename)
             file.save(os.path.join(app.config['UPLOAD_FOLDER'], secured))
             if file and secured != "":
                 addproperty = Property(request.form['title'],request.form['bedrooms'], request.form['bathrooms'], request.form['location'], request.form['price'],request.form['type'], request.form['description'],  secured)
                 db.session.add(addproperty)
                 db.session.commit()
                 flash("Your Property has been added successfully")
                 return redirect(url_for('properties'))   
    
    return render_template('create_properties.html',form=form)

@app.route('/properties/<propertyid>')
def view_property(propertyid):
    # code to retrieve the property information from the database
    # return the property information to the template
     property_info = Property.query.filter(Property.id==propertyid).all()[0]
     
     if len(property_info.bedrooms) > 1:
        bedroomlabel = 'Bedrooms'
     else:
        bedroomlabel = 'Bedroom'

     if len(property_info.bathrooms) > 1:
        bathroomlabel ='Bathrooms'
     else:
        bathroomlabel ='Bathroom'

     return render_template('property.html', singleproperty=property_info,bathlabel = bathroomlabel, bedlabel = bedroomlabel, loc=locale )


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
