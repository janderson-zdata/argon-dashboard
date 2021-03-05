# # -*- encoding: utf-8 -*-
# """
# License: MIT
# Copyright (c) 2019 - present AppSeed.us
# """

# # Python modules
# import os, logging 

# # Flask modules
# from flask               import render_template, request, url_for, redirect, send_from_directory
# from flask_login         import login_user, logout_user, current_user, login_required
# from werkzeug.exceptions import HTTPException, NotFound, abort

# # App modules
# from app        import app, lm, db, bc
# from app.models import User, Customer
# from app.forms  import LoginForm, RegisterForm, CustomerForm

# # provide login manager with load_user callback
# @lm.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# # Logout user
# @app.route('/logout.html')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

# # Customers

# @app.route('/customer/id/<int:customerId>', methods=['GET', 'POST'])
# def editCustomer(customerId):
    
#     form = CustomerForm(request.form)
#     msg = None
#     customer = Customer.query.filter_by(id=customerId).first()
#     customers = Customer.query.all()
#     if request.method == 'GET':
#         return render_template('layouts/default.html', 
#                                     content=render_template( 'pages/customers.html', form=form, msg=msg, customers=customers, customer=customer) )
#     if form.validate_on_submit():
        
#         # assign form data to variables
#         title = request.form.get('title', '', type=str)
#         gcpCustomerId = request.form.get('gcpCustomerId', '', type=str) 
#         notes    = request.form.get('notes'   , '', type=str)
#         c_id = request.form.get('id', '', type=int)
#         customerActive = True

#                 # filter customer out of database through id
#         customerUpdate = Customer.query.filter_by(id=c_id).first()
        
#         if customerUpdate:
#             #do update
#             customerUpdate.title = title
#             customerUpdate.gcpCustomerId = gcpCustomerId
#             customerUpdate.notes = notes

#             # commit change and save the object
#             db.session.commit( )

#             msg = 'Customer Updated'
#         else:
#            msg = 'Something Broke'        

#         return redirect(url_for('create', msg=msg))
        
#         # render_template('layouts/default.html', 
#         #                         content=render_template( 'pages/customers.html', form=form, msg=msg, customers=customers) )


# @app.route('/customers', methods=['GET', 'POST'])
# def create():
#     form = CustomerForm(request.form)
#     msg = request.args.get('msg')    
    
#     if request.method == 'GET':
#         customers = Customer.query.all()

#         return render_template('layouts/default.html', 
#                                 content=render_template( 'pages/customers.html', form=form, msg=msg, customers=customers) )
    
#     if form.validate_on_submit():
        
#         # assign form data to variables
#         title = request.form.get('title', '', type=str)
#         gcpCustomerId = request.form.get('gcpCustomerId', '', type=str) 
#         notes    = request.form.get('notes'   , '', type=str)
#         customerActive = True

#                 # filter customer out of database through title
#         customer = Customer.query.filter_by(title=title).first()
        
#         if customer:
#             #do update
#             customer.title = title
#             customer.gcpCustomerId = gcpCustomerId
#             customer.notes = notes

#             # commit change and save the object
#             db.session.commit( )

#             msg = 'Customer Updated'
#         else:
#             #do insert
#             customer = Customer(title, gcpCustomerId, notes)
#             customer.save()
#             msg = 'Customer Created'

#         customers = Customer.query.all()

#         return render_template('layouts/default.html', 
#                                 content=render_template( 'pages/customers.html', form=form, msg=msg, customers=customers) )
#     else:
#         return render_template('layouts/default.html', 
#                                 content=render_template( 'pages/customers.html', form=form, msg="shit broke") )
     

# # Register a new user
# @app.route('/register.html', methods=['GET', 'POST'])
# def register():
    
#     # declare the Registration Form
#     form = RegisterForm(request.form)

#     msg = None

#     if request.method == 'GET': 

#         return render_template('layouts/auth-default.html',
#                                 content=render_template( 'pages/register.html', form=form, msg=msg ) )

#     # check if both http method is POST and form is valid on submit
#     if form.validate_on_submit():

#         # assign form data to variables
#         username = request.form.get('username', '', type=str)
#         password = request.form.get('password', '', type=str) 
#         email    = request.form.get('email'   , '', type=str) 

#         # filter User out of database through username
#         user = User.query.filter_by(user=username).first()

#         # filter User out of database through username
#         user_by_email = User.query.filter_by(email=email).first()

#         if user or user_by_email:
#             msg = 'Error: User exists!'
        
#         else:         

#             pw_hash = password #bc.generate_password_hash(password)

#             user = User(username, email, pw_hash)

#             user.save()

#             msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

#     else:
#         msg = 'Input error'    

#     return render_template('layouts/auth-default.html',
#                             content=render_template( 'pages/register.html', form=form, msg=msg ) )

# # Authenticate user
# @app.route('/login.html', methods=['GET', 'POST'])
# def login():
    
#     # Declare the login form
#     form = LoginForm(request.form)

#     # Flask message injected into the page, in case of any errors
#     msg = None

#     # check if both http method is POST and form is valid on submit
#     if form.validate_on_submit():

#         # assign form data to variables
#         username = request.form.get('username', '', type=str)
#         password = request.form.get('password', '', type=str) 

#         # filter User out of database through username
#         user = User.query.filter_by(user=username).first()

#         if user:
            
#             #if bc.check_password_hash(user.password, password):
#             if user.password == password:
#                 login_user(user)
#                 return redirect(url_for('index'))
#             else:
#                 msg = "Wrong password. Please try again."
#         else:
#             msg = "Unkkown user"

#     return render_template('layouts/auth-default.html',
#                             content=render_template( 'pages/login.html', form=form, msg=msg ) )

# # App main route + generic routing
# @app.route('/', defaults={'path': 'index.html'})
# @app.route('/<path>')
# def index(path):

#     if not current_user.is_authenticated:
#         return redirect(url_for('login'))

#     content = None

#     try:

#         # try to match the pages defined in -> pages/<input file>
#         return render_template('layouts/default.html',
#                                 content=render_template( 'pages/'+path) )
#     except:
        
#         return render_template('layouts/auth-default.html',
#                                 content=render_template( 'pages/404.html' ) )

# # Return sitemap 
# @app.route('/sitemap.xml')
# def sitemap():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')
