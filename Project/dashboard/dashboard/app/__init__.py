from flask import Flask 
from flask.helpers import get_root_path
from config import BaseConfig 
import dash_bootstrap_components as dbc
import dash
# from flask_login import login_required

def create_app():
    server = Flask(__name__,instance_relative_config=False)
    server.config.from_object(BaseConfig)
    
    with server.app_context():
        register_dashapp(server)
        return server


def register_dashapp(app):
    from app.geo.layout import geo_page
    from app.geo.callbacks import register_callbacks_geomarketing




    # Meta tags for viewport responsivebess

    meta_viewport = {
        "name" : "viewport",
        "content" : "width=device-width"
    }


    geo = dash.Dash(__name__,
                        server=app,
                        url_base_pathname='/geo/',
                        assets_folder=get_root_path(__name__)+ '/assets/',
                        meta_tags=[meta_viewport])
                        # external_stylesheets=[dbc.themes.SANDSTONE])
    with app.app_context():

        geo.title = 'BIAT Geomarketing Dashboard'
        geo.layout = geo_page
        # geo._favicon = 'favicon.png'
        register_callbacks_geomarketing(geo)


    # __protect_dashviews(dashapp)
        

# def __protect_dashviews(dashapp) :
#     for view_func in dashapp.server.view_functions:
#         if view_func.startwith(dashapp.config.url_base_pathname):
#             dashapp.server.view_functions[view_func] = login_required(
#                 dashapp.server.view_functions[view_func]
#             )