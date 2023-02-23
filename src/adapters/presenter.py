from flask import jsonify


def parse_to_json(obj):

    try:
        print("try block")
        return jsonify(obj)
    except Exception as e:
        print("except block")
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500
