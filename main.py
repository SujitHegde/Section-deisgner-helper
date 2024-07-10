from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)


class Usage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    user = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.String(80), nullable=False)

# Function to initialize the database
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized.")


# Route to handle incoming data
@app.route('/track', methods=['POST'])
def track_usage():
    try:
        data = request.json
        event = data.get('e')
        timestamp = data.get('timestamp')
        user=data.get('user')
        print(f"Received data: event: {event}, timestamp: {timestamp},user:{user}")
        
        new_usage = Usage(event=event, user=user, timestamp=timestamp)
        db.session.add(new_usage)
        db.session.commit()
        dblist = Usage.query.all()
        for item in dblist:
            print(f"ID: {item.id}, Event: {item.event}, User: {item.user}, Timestamp: {item.timestamp}")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    
