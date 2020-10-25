#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import sys
import os
import dictfier
from sqlalchemy import func
from marshmallow_sqlalchemy import ModelSchema


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://fsnd:fsnd@35.208.39.244:5432/fsnd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app, session_options={"expire_on_commit":False})
ma = Marshmallow(app)
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean,default=True,nullable=True)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(250), nullable = True)


    def __repr__(self):
      return f'<Venue {self.id} {self.name} >'



    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean,default=True, nullable=True)
    seeking_description = db.Column(db.String(500))

    def __repr__(self):
      return f'<Artist {self.id} {self.name} >'

class Show(db.Model):
    __tablename__='Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable=False)
    artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'),nullable=False)
    eventdate = db.Column(db.DateTime,nullable=False)

    def __repr__(self):
      return f'<Show {self.id}>'


class VenueSchema(ModelSchema):
  class Meta:
    model = Venue

class ArtistSchema(ModelSchema):
  class Meta:
    model = Artist

class ShowSchema(ModelSchema):
  class Meta:
    model = Show

"""
venue1 = Venue(name="The Musical Hop",city="San Francisco",state="CA",address="1015 Folsom Street",phone="123-123-1234",image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",facebook_link="https://www.facebook.com/TheMusicalHop",seeking_talent=True,seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.',website="https://www.themusicalhop.com")
venue2 = Venue(name="Park Square Live Music & Coffee",city="San Francisco",state="CA",address="34 Whiskey moore ave",phone="415-000-1234",image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",seeking_talent=True,seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.',website="https://www.parksquarelivemusicandcoffee.com")
venue3 = Venue(name="The Dueling Pianos Bar",city="New York",state="NY",address="335 Delancey Street",phone="914-003-1132",image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",facebook_link="https://www.facebook.com/theduelingpianos",seeking_talent=True,seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.',website="https://www.theduelingpianos.com")

artist1_img_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
artist2_img_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
artist3_img_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"

artist1 = Artist(name="Guns N Petals",state="New York",city="NY",genres="['Rock n Roll']",image_link=artist1_img_link)
artist2 = Artist(name="Matt Quevedo",state="Delaware",city="Dover",genres="['Jazz']",image_link=artist2_img_link)
artist3 = Artist(name="The Wild Sax Band",state="Delaware",city="Dover",genres="['Jazz','Classical']",image_link=artist3_img_link)

show1 = Show(artist_id=7,venue_id=9,eventdate="2019-05-21T21:30:00.000Z")
show2 = Show(artist_id=8,venue_id=8,eventdate="2019-05-19T21:30:00.000Z")
show3 = Show(artist_id=9,venue_id=7,eventdate="2019-05-25T21:30:00.000Z")
show4 = Show(artist_id=7,venue_id=9,eventdate="2021-05-21T21:30:00.000Z")
show5 = Show(artist_id=8,venue_id=8,eventdate="2021-05-19T21:30:00.000Z")
show6 = Show(artist_id=9,venue_id=7,eventdate="2020-12-25T21:30:00.000Z")

try:
  #db.session.add(venue1)
  #db.session.add(venue2)
  #db.session.add(venue3)
  #db.session.add(artist1)
  #db.session.add(artist2)
  #db.session.add(artist3)
  #db.session.commit()

  db.session.add(show1)
  db.session.add(show2)
  db.session.add(show3)
  db.session.add(show4)
  db.session.add(show5)
  db.session.add(show6)

  db.session.commit()
except:
   db.session.rollback()
   error=True
  #print(sys.exc_info())

finally:
  print('Close')
  db.session.close()
"""

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format,locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  #venue_query = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  data = []
  city_and_state = ''
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  #show_query = Show.query.filter(Show.eventdate < current_time).all()

  #venue_query = db.session.query(Venue,Show).join(Show).filter(Show.eventdate < current_time).order_by(Venue.id).all()
  #venue_query = db.session.query(Venue,Show).join(Show).filter(Show.eventdate < current_time).order_by(Venue.id).all()
  #venue_query = db.session.query(Venue.city,Venue.state,Show.venue_id,Venue.name,db.func.count(Show.venue_id)).join(Show, Show.venue_id == Venue.id).filter(Show.eventdate > current_time).group_by(Venue.city,Venue.state,Show.venue_id,Venue.name).all()

  #venue_query = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()

  venue_query = db.session.query(Venue.city,Venue.state,Show.venue_id,Venue.name,db.func.count(Show.venue_id).label('upcoming_shows')).join(Show, Show.venue_id == Venue.id).filter(Show.eventdate > current_time).group_by(Venue.city,Venue.state,Show.venue_id,Venue.name).all()
  
  for venue in venue_query:
    upcoming_shows = venue.upcoming_shows

    if city_and_state == venue.city + venue.state:
      
      data[len(data) - 1]["venues"].append({
        "id": venue.venue_id,
        "name": venue.name,
        "num_upcoming_shows": upcoming_shows
        })
    else:
      city_and_state = venue.city + venue.state
      data.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [{
        "id": venue.venue_id,
        "name": venue.name,
        "num_upcoming_shows": upcoming_shows
        }]
        })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  """
  term = search_term=request.form.get('search_term')
  print('----serch term----')
  print(term)

  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }

  venue_query = db.session.query(Venue.city,Venue.state,Show.venue_id,Venue.name,db.func.count(Show.venue_id).label('upcoming_shows')).join(Show, Show.venue_id == Venue.id).filter(Show.eventdate > current_time).group_by(Venue.city,Venue.state,Show.venue_id,Venue.name).all()
  """

  search_term = request.form.get('search_term', '')
  result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  response = {
  "count": result.count(),
  "data": result
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  v_id = venue_id
  vid_query = db.session.query(Venue.city,Venue.website,Venue.facebook_link,Venue.seeking_talent,Venue.seeking_description,Venue.state,Venue.address,Show.venue_id.label("venue_id"),Venue.name.label("venue_name"),Venue.address.label("address"),Venue.phone,Venue.image_link).join(Show, Show.venue_id == Venue.id).filter(Show.venue_id == v_id).all()

  data = []
  
  for VI in vid_query:
    data = {
    "id" : VI.venue_id,
    "name": VI.venue_name,
    'genres': ['Jazz', 'Reggae', 'Swing', 'Classical'],
    "address" : VI.address,
    "city" : VI.city,
    "state" : VI.state,
    "phone" : VI.phone,
    "website" : VI.website,
    "facebook_link" : VI.facebook_link,
    "seeking_talent" : VI.seeking_talent,
    "seeking_description" : VI.seeking_description,
    "image_link" : VI.image_link
    }

  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  address = request.form['address']

  if len(city) > 120:
    flash('Length of city should be less than or equal to 120')
    return render_template('pages/home.html')
  elif len(state) > 120:
    flash('Length of state should be less than or equal to 120')
    return render_template('pages/home.html')
  elif len(phone) > 120:
    flash('Length of phone should be less than or equal to 120')
    return render_template('pages/home.html')
  elif len(address) > 120:
    flash('Length of address should be less than or equal to 120')
    return render_template('pages/home.html')
  else:
    venue1 = Venue(name=name,state=state,city=city,phone=phone,address=address)
    db.session.add(venue1)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.filter_by(id=venue_id).first_or_404()
    db.session.delete(venue)
    db.session.commit()
    flash('The venue has been removed together with all of its shows.')
    return render_template('pages/home.html')
  except ValueError:
    flash('It was not possible to delete this Venue')
    return render_template('pages/home.html')
    

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artist_query = Artist.query.group_by(Artist.id, Artist.name).all()

  data = []

  for A in artist_query:
    record = {
    'id': A.id,
    'name': A.name}

    data.append(record)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  """
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  """

  search_term = request.form.get('search_term', '')
  result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  response = {
  "count": result.count(),
  "data": result
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  a_id = artist_id

  aid_query = db.session.query(Artist).filter(Artist.id==a_id).all()

  data = []

  for A in aid_query:
    data = {
    "id": A.id,
    "name": A.name,
    "genres": A.genres,
    "city": A.city,
    "state": A.state,
    "phone": A.phone,
    "image_link": A.image_link,
    "facebook_link": A.facebook_link,
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!"}
  
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']

  artist1 = Artist(name=name,state=state,city=city,phone=phone)
  db.session.add(artist1)
  db.session.commit()

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  show_query = db.session.query(Show.venue_id,Venue.name.label("venue_name"),Artist.id.label("artist_id"),Artist.name.label("artist_name"),Artist.image_link,Show.eventdate).join(Venue, Show.venue_id == Venue.id).join(Artist, Show.artist_id==Artist.id).filter(Show.eventdate > current_time).all()
  
  data = []

  for S in show_query:
    record = {
    "venue_id" : S.venue_id,
    "venue_name" : S.venue_name,
    "artist_id" : S.artist_id,
    "artist_name" : S.artist_name,
    "artist_image_link" : S.image_link,
    "start_time" : str(S.eventdate)
    }

    data.append(record)
  

  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  aid = request.form['artist_id']
  vid = request.form['venue_id']
  eventdate = request.form['start_time']
  show1 = Show(artist_id=aid,venue_id=vid,eventdate=eventdate)
  db.session.add(show1)
  db.session.commit()

  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
