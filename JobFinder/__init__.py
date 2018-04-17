from flask import Flask
app = Flask(__name__)
from JobFinder.Controllers import controller
