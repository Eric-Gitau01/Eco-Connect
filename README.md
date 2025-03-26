# Eco-Connect
# Introduction
Eco-Connect is a community focused platform designed to connect people with their neighbours in the pursuit of a clean and sustainable environment. Together, they can identify opportunities for improvement and recognize the positive environmental practices already in place. Eco-Connect fosters a sense of shared responsibility, ensuring a healthy and thriving environment for everyone.

# Features
Community Engagement: Connect with neighbours to promote sustainability.
Environmental Awareness: Identify and share eco-friendly practices.
Collaborative Efforts: Work together to improve local environmental conditions.
User Friendly Interface: Easy-to-use platform for seamless interaction.

# Technologies and Dependancies
Backend: Flask - Python
Database: SQLAlchemy - with Flask-SQLAlchemy
Migrations: Flask-Migrate
Environment Management: python-dotenv
Database Driver: PyMySQL

# Installation ans Setup
**Clone the Repository**
git  clone https://github.com/FionaGachuuri/Eco-Connect.git
cd Eco-Connect
**Set up Virtual Environment**
python -m venv venv
source venv/bin/activate 
**Install Dependencies**
pip install -r requirements.txt
**Configure Environment Variables**
Create a .env file in the root directory.
**Run Database Migrations**
flask db init
flask db migrate
flask db upgrade
**Start the Application**
flask run

# Contact
Author: Fiona Gachuuri
Github: FionaGachuuri
Email: fionairuka@gmail.com

# Contributing
Fork the repository.
Create a new branch.
Commit your changes. 
Push to the branch.
Open a Pull Request.
