# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from app         import db

class User(UserMixin, db.Model):

    id       = db.Column(db.Integer,     primary_key=True)
    user     = db.Column(db.String(64),  unique = True)
    email    = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(500))

    def __init__(self, user, email, password):
        self.user       = user
        self.password   = password
        self.email      = email

    def __repr__(self):
        return '<User %r - %s>' % (self.id) % (self.email)

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    gcpCustomerId  = db.Column(db.String(256))
    notes = db.Column(db.String(2000))
    customerActive = db.Column(db.Boolean)

    def __init__(self, title, gcpCustomerId, notes):
        self.title = title
        self.gcpCustomerId = gcpCustomerId
        self.notes = notes
        self.customerActive = True

    def __repr__(self):
        return f'Customer("{self.title}","{self.gcpCustomerId}","{self.notes}")'

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship("Customer")
    product = db.Column(db.String(256))
    productDescription = db.Column(db.String(2000))
    begainDate = db.Column(db.DateTime(), nullable = False)
    endDate = db.Column(db.DateTime(), nullable = False)

    def __init__(self, customerId, product, productDescription, begainDate, endDate):
        self.customerId = customerId
        self.product = product
        self.productDescription = productDescription
        self.begainDate = begainDate
        self.endDate = endDate
    
    def __repr__(self):
        return f'Contract("{self.customerId}","{self.product}","{self.productDescription}", {self.begainDate}, {self.endDate})'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class BillingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submittedRecord = db.Column(db.String(256))
    customerId = db.Column(db.Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship("Customer")
    submittedOn = db.Column(db.DateTime(), nullable = False)
    wasSuccessful = db.Column(db.Boolean(), nullable=False)

    def __init__(self, submittedRecord, customerId, wasSuccessful):
        self.submittedRecord = submittedRecord
        self.wasSuccessful = wasSuccessful
        self.customerId = customerId
        self.submittedOn = datetime.now()
           
    def __repr__(self):
        return '<Record %r - %s>' % (self.submittedRecord) % (self.wasSuccessful)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class GCPRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productid = db.Column(db.String(256))
    customerid = db.Column(db.String(256))
    dimension = db.Column(db.String(256))
    value_type = db.Column(db.String(256))
    value = db.Column(db.Integer)

    def __init__(self, productid, customerid, dimension, value):
        self.productid = productid
        self.customerid = customerid
        self.dimension = dimension
        self.value = value
        self.value_type = "int64"
   
    def __repr__(self):
        return 'test'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self