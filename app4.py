from flask import Flask, render_template

app = Flask(__name__)

technologies = [
    { "name": "Aston Villa Football top", "price": "£59.99", "description": "Claret and Blue top to represtent ASVFC.", "image": "/static/aston-villa.jpg", "shirtindex": "0" },
    { "name": "Plymouth Argyle Football top", "price": "£44.99", "description": "Plymouth Argyle.","image": "/static/plymouth.jpg", "shirtindex": "1" },
    { "name": "Nottingham football top", "price": "£54.99", "description": "Nottingham FC.", "image": "/static/nottingham.jpg", "shirtindex": "2" },
]

@app.route('/test2/', methods=['GET'])
def options():
    choices =['1', '2', '3', '4']
    return render_template('test2.html', choices = choices)
    



@app.route('/')
def galleryPage():
    return render_template('index.html',technologies = technologies,colours=["low-price","highest-price","a-z","z-a"])
    #if colours selected == 'low price':
     #   sort technologies by lowest price to highest
            

    #repeat for highest price
    #sort by a-z
    #sort by z-a
            #if request.method =='POST':
     #   low_price = int(request.form['lowest_price'])
      #  if lowest_price > 0:
       #     filterd = [item for item in tech_data if item['price']>= lowest_price]

@app.route('/tech/<int:techId>')
def singleProductPage(techId):
    return render_template('SingleTech.html', technology = technologies[techId])


@app.route('/test1', methods=['GET', 'POST'])
def test1():
    colours = ['red', 'blue']   
    return render_template('test1.html', colours = colours)
    

if __name__ == '__main__':
    app.run(debug=True)

#https://memudualimatou.medium.com/creating-a-select-tag-on-a-web-application-using-flask-python-fffe6ea0c939
##view-source:http://127.0.0.1:5000/