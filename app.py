from openai import OpenAI
from flask import Flask, request, jsonify, send_from_directory
import mysql.connector

app = Flask(__name__)

client = OpenAI(api_key='')

messages = [{"role": "system", "content": "You are a healthcare assistant to assist the patients to "
                                          "get better healthcare,"
                                          " you should just answer the question related to healthcare,"
                                          " and if your input question wasn't "
                                          "about healthcare and relatives you should say "
                                          "I'm sorry i just can assist you with your healthcare problem"}]


db_config = {
    'port': 3306,
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'healthcare_assistance'
}

db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        role VARCHAR(255),
        content TEXT
    )
""")
db_connection.commit()

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json['user_input']
    messages.append({"role": "user", "content": user_input})
    
    db_cursor.execute("""
        INSERT INTO messages (role, content)
        VALUES (%s, %s)
    """, ('user', user_input))
    db_connection.commit()
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages)
    ChatGPT_reply = response.choices[0].message.content

    db_cursor.execute("""
        INSERT INTO messages (role, content)
        VALUES (%s, %s)
    """, ('assistant', ChatGPT_reply))
    db_connection.commit()
    
    return jsonify({"reply": ChatGPT_reply})


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/fetch_messages', methods=['GET'])
def fetch_messages():
    db_cursor.execute("""
        SELECT content FROM messages WHERE role = 'user'
    """)
    user_messages = db_cursor.fetchall()
    return jsonify({"user_messages": user_messages})

if __name__ == '__main__':
    app.run(debug=True)