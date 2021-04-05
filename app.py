# render flask templates, bootstraps and import files for routing and module use
from flask import Flask, render_template, url_for, request, abort, Response
from flask_bootstrap import Bootstrap
from q_one import *
from q_two import *
from q_three import *
from q_four import *
from q_five import *
from q_six import *
from q_seven import *
from q_eight import *
from q_nine import *

app = Flask(__name__)

# for base bootstrap styling
Bootstrap(app)

# for index route - home page
@app.route('/')
def index():
    return render_template('index.html')

# for question one route page
@app.route('/qone')
def qone():
  return render_template('qone.html', most_popular_html = most_popular_html)

# for question two page
@app.route('/qtwo')
def qtwo():
  return render_template('qtwo.html', return_customer_html = return_customer_html, return_customer_count_html = return_customer_count_html)

# for question three page
@app.route('/qthree')
def qthree():
  return render_template('qthree.html', sales_by_order_id_html = sales_by_order_id_html, sales_by_dollar_html = sales_by_dollar_html)

# for question four page
@app.route('/qfour')
def qfour():
  return render_template('qfour.html', shipper_mean_orders_html = shipper_mean_orders_html, shipper_mean_order_details_html = shipper_mean_order_details_html)

# for question five page
@app.route('/qfive')
def qfive():
  return render_template('qfive.html', top_two_employees_html = top_two_employees_html)

# for question six page
@app.route('/qsix')
def qsix():
  return render_template('qsix.html', most_supplier_html = most_supplier_html, supplier_list_html = supplier_list_html)

# for question seven page
@app.route('/qseven')
def qseven():
  return render_template('qseven.html', shpping_mean_html = shpping_mean_html, shpping_list_html = shpping_list_html)

# for question eight page
@app.route('/qeight')
def qeight():
  return render_template('qeight.html', shpping_mean_customer_html = shpping_mean_customer_html, shpping_list_customer_html = shpping_list_customer_html)

# for question nine page
@app.route('/qnine')
def qnine():
  return render_template('qnine.html')

# port localhost 5000 for deploy
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')