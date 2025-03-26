from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('landingpage.html')

@home_bp.route('/login.html')
def login():
    return render_template('login.html')

@home_bp.route('/report_issue.html')
def report_issue():
    return render_template('report_issue.html')

@home_bp.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')
