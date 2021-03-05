# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField, DateField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	username    = StringField  (u'Username'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email()])

class CustomerForm(FlaskForm):
	title 		= StringField  (u'title'  , validators=[DataRequired()])
	gcpCustomerId  = StringField  (u'gcpCustomerId'  , validators=[DataRequired()])
	notes 		= TextAreaField  (u'notes'  , validators=[DataRequired()])

class ContractForm(FlaskForm):
	product 		= StringField  (u'product'  , validators=[DataRequired()])
	productDescription  = StringField  (u'productDescription'  , validators=[DataRequired()])
	customerId = SelectField  (u'customerId'  , validators=[DataRequired()])
	begainDate	= DateField  (u'begainDate'  , validators=[DataRequired()])
	endDate	= DateField  (u'endDate'  , validators=[DataRequired()])


