# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging 

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app        import app, lm, db, bc
from app.models import Customer
from app.forms  import CustomerForm

# Customers
@app.route('/customer/id/<int:customerId>', methods=['GET', 'POST'])
def editCustomer(customerId):
    
    form = CustomerForm(request.form)
    msg = None
    customer = Customer.query.filter_by(id=customerId).first()
    customers = Customer.query.all()
    if request.method == 'GET':
        return render_template('layouts/default.html', 
                                    content=render_template( 'pages/customers.html', form=form, msg=msg, customers=customers, customer=customer) )
    if form.validate_on_submit():
        
        # assign form data to variables
        title = request.form.get('title', '', type=str)
        gcpCustomerId = request.form.get('gcpCustomerId', '', type=str) 
        notes    = request.form.get('notes'   , '', type=str)
        c_id = request.form.get('id', '', type=int)
        customerActive = True

                # filter customer out of database through id
        customer_update = Customer.query.filter_by(id=c_id).first()
        
        if customer_update:
            #do update
            customer_update.title = title
            customer_update.gcpCustomerId = gcpCustomerId
            customer_update.notes = notes

            # commit change and save the object
            db.session.commit( )

            msg = 'Customer Updated'
        else:
            msg = 'Something Broke'

        return redirect(url_for('create', msg=msg))
        
@app.route('/customers', methods=['GET', 'POST'])
def create():
    form = CustomerForm(request.form)
    msg = request.args.get('msg')    
    
    if request.method == 'GET':
        customers = Customer.query.all()

        return render_template('layouts/default.html', 
                                content=render_template( 'pages/customers.html', form=form, msg=msg, customers=customers) )
    
    if form.validate_on_submit():
        
        # assign form data to variables
        title = request.form.get('title', '', type=str)
        gcpCustomerId = request.form.get('gcpCustomerId', '', type=str) 
        notes    = request.form.get('notes'   , '', type=str)
        customerActive = True

                # filter customer out of database through title
        customer = Customer.query.filter_by(title=title).first()
        
        if customer:
            #do update
            customer.title = title
            customer.gcpCustomerId = gcpCustomerId
            customer.notes = notes

            # commit change and save the object
            db.session.commit( )

            msg = 'Customer Updated'
        else:
            #do insert
            customer = Customer(title, gcpCustomerId, notes)
            customer.save()
            msg = 'Customer Created'

        customers = Customer.query.all()

        return render_template('layouts/default.html', 
                                content=render_template( 'pages/customers.html', form=form, msg=msg, customers=customers) )
    else:
        return render_template('layouts/default.html', 
                                content=render_template( 'pages/customers.html', form=form, msg="shit broke") )
   

