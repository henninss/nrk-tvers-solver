from flask import Flask
from asgiref.wsgi import WsgiToAsgi

from app import app

asgi_app = WsgiToAsgi(app)

