# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: webserver_restaurants
 * Date: 2/4/16
 * Time: 10:46
 * To change this template use File | Settings | File Templates.
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants Menu</h1>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    # Objective 2 -- Add Edit and Delete links
                    output += "<a href=/restaurants/{}/edit>Edit</a>".format(
                        restaurant.id
                    )
                    output += "</br>"
                    output += "<a href=/restaurants/{}/delete>" \
                              "Delete</a>".format(restaurant.id)
                    output += "</br></br></br>"
                output += "<a href='/restaurants/new'>" \
                          "Make a New Restaurant</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            # Objective 3 Step 2 - Create /restarants/new page
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data'" \
                          " action='/restaurants/new'>" \
                          "  Restaurant name:<br>" \
                          "  <input type='text' name='restaurant_name'" \
                          "placeholder = 'New Restaurant Name'><br>" \
                          "  <input type='submit' value='Create'>" \
                          "</form>"
                output += "</br></br></br>"
                output += "<a href='/restaurants'>Home</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            # Objective 4 - Create /restaurants/<id_number>/edit page
            if self.path.endswith("/edit"):
                input_id = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(
                    id=input_id).one()
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>{}</h1>".format(restaurant.name)
                    output += "<form method='POST' " \
                              "enctype='multipart/form-data'" \
                              " action='/restaurants/{0}/edit'>" \
                              "  New Restaurant name:<br>" \
                              "  <input type='text' " \
                              "name='restaurant_edit_name'" \
                              "placeholder = {1}><br>" \
                              "  <input type='submit' value='Rename'>" \
                              "</form>".format(input_id, restaurant.name)
                    output += "</br></br></br>"
                    output += "<a href='/restaurants'>Home</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print(output)
                    return
            # Objective 5 - Create /restaurants/<id_number>/delete page
            if self.path.endswith("/delete"):
                input_id = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(
                    id=input_id).one()
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete " \
                              "{0}?</h1>".format(restaurant.name)
                    output += "<form method='POST' " \
                              "enctype='multipart/form-data'" \
                              " action='/restaurants/{0}/delete'>" \
                              " <input type='submit' value='Delete'>" \
                              "</form>".format(input_id)
                    output += "</br></br></br>"
                    output += "<a href='/restaurants'>Home</a>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print(output)
                    return
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant_name')
                # Create a new restaurant object
                new_restaurant = Restaurant(name=restaurant_name[0])
                session.add(new_restaurant)
                session.commit()
                print("New restaurant {} created!".format(restaurant_name[0]))
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            # Objective 4 - Edit POST
            if self.path.endswith("/edit"):
                input_id = self.path.split("/")[2]
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant_edit_name')
                # Get the restaurant to edit
                restaurant = session.query(Restaurant).filter_by(
                    id=input_id).one()
                if restaurant:
                    old_name = restaurant.name
                    restaurant.name = restaurant_name[0]
                    session.add(restaurant)
                    session.commit()
                    print("Restaurant {0} changer to {1}!".format(
                        old_name, restaurant_name[0]))

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            # Objective 5 - Delete POST
            if self.path.endswith("/delete"):
                input_id = self.path.split("/")[2]
                # Get the restaurant to delete
                restaurant = session.query(Restaurant).filter_by(
                    id=input_id).one()
                if restaurant:
                    session.delete(restaurant)
                    session.commit()
                    print("Restaurant {0} deleted!".format(restaurant.name))
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server running... Open localhost:{0}/restaurants "
              "in your browser".format(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, shutting down server...")
        server.socket.close()


if __name__ == "__main__":
    main()
