from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_license', methods=['POST'])
def plan_route():
    time.sleep(2)

    journey_data = request.form.to_dict()
    print(journey_data)
    # TODO: call APIs
    
    # Dummy response data
    response_data = {
        'status': 'success',
        'journey_plan': "<strong>License Number:</strong> ABC123456<br><strong>Owner:</strong> John Doe<br><br><strong>Accident Cases:</strong> 5<br><strong>Insurance Status:</strong> Not Insured"
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
