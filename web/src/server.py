from wsgiref.simple_server import make_server
from pyramid.response import Response
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from datetime import datetime
import mysql.connector as mysql
import bjoern
import json
import os

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

def add_visitor(req):
  info = req.json_body
  info_list = [str(info['f']), str(info['e']), str(info['c'])]
  time = str(datetime.now())
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  sql = """INSERT INTO Users (
    name, email, comment, created_at)
    VALUES (%s, %s, %s, %s)"""
  val = (info_list[0], info_list[1], info_list[2], time)
  cursor.execute(sql, val)
  db.commit()

def get_home(req):
  return render_to_response('templates/home.html', [], request=req)

def welcome(req):
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  cursor.execute("SELECT name, created_at, comment FROM Users")
  data = cursor.fetchall()
  db.close()
  return render_to_response('templates/welcome.html', {'visitors': data}, request=req)

def about(req):
  return render_to_response('templates/about.html', [], request=req)

def cv(req):
  return render_to_response('templates/cv.html', [], request=req)

def avatar(req):
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  cursor.execute("SELECT avatar FROM Users")
  data = cursor.fetchall()
  db.close()

  theData = {"image_src": data[0][0]}
  response = Response(body=json.dumps(theData))
  response.headers.update({'Access-Control-Allow-Origin': '*',})
  return response

def personal(req):
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  cursor.execute("SELECT name, email FROM Users")
  data = cursor.fetchall()
  db.close()

  theData = {"name": data[0][0], "email":data[0][1]}
  response = Response(body=json.dumps(theData))
  response.headers.update({'Access-Control-Allow-Origin': '*',})
  return response

def education(req):
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  cursor.execute("SELECT school, degree, major, date FROM Users")
  data = cursor.fetchall()
  db.close()

  theData = {"school": data[0][0], "degree": data[0][1], "major": data[0][2],"date": data[0][3]}
  response = Response(body=json.dumps(theData))
  response.headers.update({'Access-Control-Allow-Origin': '*',})
  return response

def project(req):
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  cursor.execute("SELECT title, description, link, image_src, team FROM Users")
  data = cursor.fetchall()
  db.close()

  theData = {"title": data[0][0], "description": data[0][1], "link": data[0][2], "image_src": data[0][3], "team": data[0][4]}
  response = Response(body=json.dumps(theData))
  response.headers.update({'Access-Control-Allow-Origin': '*',})
  return response

''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('add_visitor', '/add_visitor')
  config.add_view(add_visitor, route_name='add_visitor', renderer='json')

  config.add_route('get_home', '/')
  config.add_view(get_home, route_name='get_home')

  config.add_route('welcome', '/welcome')
  config.add_view(welcome, route_name='welcome')

  config.add_route('about', '/about')
  config.add_view(about, route_name='about')

  config.add_route('cv', '/cv')
  config.add_view(cv, route_name='cv')

  config.add_route('avatar', '/avatar')
  config.add_view(avatar, route_name='avatar', renderer='json')

  config.add_route('personal', '/personal')
  config.add_view(personal, route_name='personal', renderer='json')

  config.add_route('education', '/education')
  config.add_view(education, route_name='education', renderer='json')

  config.add_route('project', '/project')
  config.add_view(project, route_name='project', renderer='json')

  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  bjoern.run(app, "0.0.0.0", 6000)
