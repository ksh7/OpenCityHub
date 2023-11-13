from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan_route', methods=['POST'])
def plan_route():
    time.sleep(2)

    journey_data = request.form.to_dict()
    # TODO: call APIs
    
    # Dummy response data
    response_data = {
        'status': 'success',
        'journey_plan': "Embark from Broadway, opting for the metro to Fifth Avenue to bypass heavy traffic. Cycle to Wall Street for a scenic route. Transition to a car for the final leg to Madison Avenue, anticipating lighter traffic conditions. Enjoy a versatile journey, seamlessly navigating New York's dynamic streetscape. Safe travels!"
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
