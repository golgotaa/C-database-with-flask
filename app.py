from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# SQL Server connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=' + \
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-NNFU23VJ\\SQLKO;' + \
    'DATABASE=FinanceDB;Trusted_Connection=yes;TrustServerCertificate=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Categories(db.Model):
    __tablename__ = 'Categories'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Categories.query.all()
    return jsonify([{
        'id': category.id,
        'amount': category.amount,
        'type': category.type,
        'description': category.description,
        'date': category.date
    } for category in categories])

@app.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    if data['type'] not in ['Income', 'Expense']:
        return jsonify({'message': 'Invalid category type'}), 400
    
    new_category = Categories(
        amount=data['amount'],
        type=data['type'],
        description=data.get('description'),
        date=datetime.strptime(data['date'], '%Y-%m-%d')
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category added'}), 201

@app.route('/categories/search', methods=['GET'])
def search_categories():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not start_date or not end_date:
        return jsonify({'message': 'Start date and end date are required'}), 400

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    categories = Categories.query.all()
    sorted_categories = sorted(categories, key=lambda x: x.date)

    # Binary search to find the start and end indices
    def find_index(date, find_start=True):
        low, high = 0, len(sorted_categories) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_date = sorted_categories[mid].date
            if mid_date < date:
                low = mid + 1
            elif mid_date > date:
                high = mid - 1
            else:
                if find_start:
                    if mid == 0 or sorted_categories[mid - 1].date < date:
                        return mid
                    high = mid - 1
                else:
                    if mid == len(sorted_categories) - 1 or sorted_categories[mid + 1].date > date:
                        return mid
                    low = mid + 1
        return low if find_start else high

    start_index = find_index(start_date, find_start=True)
    end_index = find_index(end_date, find_start=False)

    filtered_categories = sorted_categories[start_index:end_index+1]

    return jsonify([{
        'id': category.id,
        'amount': category.amount,
        'type': category.type,
        'description': category.description,
        'date': category.date
    } for category in filtered_categories])

@app.route('/categories/all')
def all_categories():
    return render_template('all_categories.php')

if __name__ == '__main__':
    app.run(debug=True)
