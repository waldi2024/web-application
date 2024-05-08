from flask import Flask, g, render_template, request, redirect, url_for, session, redirect, url_for, session, flash
from flask  import get_flashed_messages
import sqlite3
import random


app = Flask(__name__)
app.config["SECRET_KEY"]="thefootballstoresecreykey=3"


 # connect to database.db
def connect_db():
    sql=sqlite3.connect('./database.db')
    sql.row_factory=sqlite3.Row
    return sql
    
    # store database details in global space (g)
def get_db():
    if not hasattr(g,'sqlite3'):
         g.sqlite3_db=connect_db()
    return g.sqlite3_db
    
    # close database
@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite3_db'):
        g.sqlite3_db.close()


technologies = [
    { "name": "Aston Villa Football top", "price": "£59.99", "description": "Claret and Blue top to represtent ASVFC.", "image": "/static/aston-villa.jpg", "shirtindex": "0", "CO2": "4",},
    { "name": "Plymouth Argyle Football top", "price": "£44.99", "description": "Plymouth Argyle.","image": "/static/plymouth.jpg", "shirtindex": "1", "CO2": "1",},
    { "name": "Nottingham football top", "price": "£54.99", "description": "Nottingham FC.", "image": "/static/nottingham.jpg", "shirtindex": "2", "CO2": "2",},
    { "name": "Wolverhampton wanderers top", "price": "£52.99", "description": "Wolverhampton FC.", "image": "/static/wolves-1.jpg", "shirtindex": "3", "CO2": "2",},
    { "name": "west brom top", "price": "£46.99", "description": "West brom.", "image": "/static/westbrom-1.jpg", "shirtindex": "4", "CO2": "3",},
    { "name": "Cardiff football top", "price": "£42.99", "description": "Cardiff Football calub located in the United kingdom.", "image": "/static/cardiff.png", "shirtindex": "5", "CO2": "1",},
    { "name": "Manchester United football top", "price": "£74.99", "description": "Manchester United FC.", "image": "/static/manunited.webp", "shirtindex": "6", "CO2": "4",},
    { "name": "Liverpool football top", "price": "£69.99", "description": "Liverpool FC.", "image": "/static/liverpool.jpg", "shirtindex": "7", "CO2": "3",},
    { "name": "Chelsea football top", "price": "£69.99", "description": "Chelsea FC.", "image": "/static/chelsea.jpg", "shirtindex": "8", "CO2": "4",},
]


@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    description = request.form['description']
    technologies.append({"name": name, "description": description})
    return redirect(url_for('galleryPage'))

@app.route('/')
def galleryPage():
    if 'ordernumber' in session:
     ordernumber=session['ordernumber']
    else:
      ordernumber=(random.randrange(1,100000))
      session['ordernumber']=ordernumber
      session['itemnumber']=1
      session['totalprice']=0
    if 'itemnumber' in session:
      itemnumber=session['itemnumber']
    else:
      itemnumber=1
      session['itemnumber']=itemnumber
    if 'totalprice' in session:
      totalprice=session['totalprice']
    else:
      totalprice=0
      session['totalprice']=totalprice

    selected_colour = request.args.get('colour', default=None)
    if selected_colour == 'low-price':
        sorted_technologies = sorted(technologies, key=lambda x: float(x['price'].replace('£', '')))
    elif selected_colour == 'highest-price':
        sorted_technologies = sorted(technologies, key=lambda x: float(x['price'].replace('£', '')), reverse=True)
    elif selected_colour == 'a-z':
        sorted_technologies = sorted(technologies, key=lambda x: x['name'])
    elif selected_colour == 'z-a':
        sorted_technologies = sorted(technologies, key=lambda x: x['name'], reverse=True)
    elif selected_colour == 'CO2 low-high':
        sorted_technologies = sorted(technologies, key=lambda x: x['CO2'])
    elif selected_colour == 'CO2 high-low':
        sorted_technologies = sorted(technologies, key=lambda x: x['CO2'], reverse=True)
    else:
        sorted_technologies = sorted(technologies, key=lambda x: float(x['price'].replace('£', '')))
    return render_template('index.html', technologies=sorted_technologies, colours=["low-price", "highest-price", "a-z", "z-a", "CO2 high-low", "CO2 low-high"], selected_colour=selected_colour)


    
@app.route('/tech/<int:techId>', methods = ['GET'])
def singleProduct_get(techId):
    return render_template('SingleTech.html', technology = technologies[techId])

@app.route('/tech/<int:techId>', methods = ['POST'])
def singleProduct_post(techId):
    ordername=request.form["name"]
    orderprice=request.form["price"]
    orderdescription=request.form["description"]
    orderquantity=request.form["quantity"]
    ordernumber=session['ordernumber']
    orderno = ordernumber
    itemnumber=session['itemnumber']
    itemno = itemnumber
    shirtindex = request.form["name"]
    db=get_db()
    cursor=db.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)",(orderno,itemno,shirtindex,orderprice,orderquantity))
    session['itemnumber']=itemnumber+1
    totalprice=session['totalprice']
    orderprice2=orderprice[1:]  #remove £
    itemtotalprice=float(orderprice2)*int(orderquantity)
    totalprice2=totalprice+itemtotalprice
    db.commit()
    session['totalprice']=round(totalprice2,2)
    return render_template('SingleTech.html', technology = technologies[techId])


@app.route('/basket', methods = ['GET'])
def basket_get():
    ordernumber=session['ordernumber']
    ordernostr = str(ordernumber)
    db=get_db()
    result=db.execute("SELECT * FROM orders WHERE orderno = "+ordernostr).fetchall()
    db.commit()
    return render_template('basket.html', result = result)

@app.route('/basket', methods = ['POST'])
def basket_removeitem():
    ordernumber=session['ordernumber']
    ordernostr = str(ordernumber)
    itemno=request.form['submit_button']
    itemnostr=str(itemno)
    db=get_db()
    result=db.execute("DELETE FROM orders WHERE orderno= "+ordernostr+" and itemno= "+itemnostr)
    db.commit()
    db=get_db()
    result=db.execute("SELECT * FROM orders WHERE orderno = "+ordernostr).fetchall()
    db.commit()
    return render_template('basket.html', result = result)


@app.route('/checkout', methods=['GET'])
def checkout_get():
    totalprice=session['totalprice']
    print('totalprice:')
    print(totalprice)
    return render_template('checkout.html',totalprice=totalprice)


@app.route('/checkout', methods=['POST'])
def checkout_post():
    totalprice=session['totalprice']
    orderusername=request.form["name"]
    orderaccount=request.form["account"]
    orderamount=request.form["amount"]
    orderaccountcheck=orderaccount
    orderaccountcheck=orderaccountcheck.replace("-","")
    orderaccountcheck=orderaccountcheck.replace(" ","")
    message=""
    if len(orderusername)=="":
        message=message+"Please enter your name\n"
    if len(orderaccountcheck)<16:
        message=message+"Please enter your 16 digit account number\n"
    if len(orderaccountcheck)>16:
        message=message+"Please enter your 16 digit account number\n"
        
    if message=="":
        message="Order Submitted"
        ordernumber=(random.randrange(1,100000))
        session['ordernumber']=ordernumber
        session['itemnumber']=1
        session['totalprice']=0 
        totalprice=0 
        
    flash(message)
    
    return render_template('checkout.html',totalprice=totalprice)


if __name__ == '__main__':
    app.run(debug=True)