from flask import Flask, request, jsonify
from flask_cors import CORS  

app = Flask(__name__)  # Fixed from _name_ to __name__
CORS(app)

def calculate_final_grade(assignments, exams, weights, max_assignment, max_exam):
    """
    Calculate final grade based on weighted assignments and exams, capping it at 10.
    """
    assignment_weight = weights.get("assignments", 0)
    exam_weight = weights.get("exams", 0)

    if assignments:
        average_assignments = sum(assignments) / len(assignments)
        scaled_assignments = (average_assignments / max_assignment) * 10
    else:
        scaled_assignments = 0

    if exams:
        average_exams = (sum(exams) / len(exams)) * (10 / max_exam)
    else:
        average_exams = 0

    final_grade = (scaled_assignments * (assignment_weight / 100)) + (average_exams * (exam_weight / 100))

    return round(min(final_grade, 10), 2)

@app.route('/calculate_grade', methods=['POST'])
def calculate_grade():
    data = request.json

    assignments = data.get("assignments")
    exams = data.get("exams")
    weights = data.get("weights")
    max_assignment = data.get("max_assignment", 10)  # Default to 10 if not provided
    max_exam = data.get("max_exam", 100)  # Default to 100 if not provided

    if assignments is None or exams is None or weights is None:
        return jsonify({"error": "Please provide assignments, exams, weights, max_assignment, and max_exam."}), 400

    try:
        final_grade = calculate_final_grade(assignments, exams, weights, max_assignment, max_exam)
        return jsonify({"final_grade": final_grade}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Change to 0.0.0.0
