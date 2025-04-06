from typing import Union
from flasgger import Swagger
from flask import Flask, Response, jsonify

import rest_views

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

Swagger(app, config=swagger_config)


@app.route("/app/events/<int:start_time>/<int:end_time>", methods=["GET"])
def get_events_controller(start_time: int, end_time: int) -> Union[Response, tuple[Response, int]]:
    """
    Get all events within a time range
    ---
    parameters:
      - name: start_time
        in: path
        type: integer
        format: int64
        required: true
        description: Start timestamp in nanoseconds
      - name: end_time
        in: path
        type: integer
        format: int64
        required: true
        description: End timestamp in nanoseconds
    responses:
      200:
        description: List of events with records within the specified time range
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: Event ID
              name:
                type: string
                description: Event name
              records:
                type: array
                items:
                  type: array
                  items:
                    type: integer
                    format: int64
                    description: [timestamp in nanoseconds, data]
    """

    try:
        events = rest_views.get_events_controller(start_time, end_time)
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/app/events/<int:event_id>/<int:start_time>/<int:end_time>", methods=["GET"])
def get_event_by_id_controller(event_id: int, start_time: int, end_time: int) -> Union[tuple[Response, int], Response]:
    """
    Get a specific event by ID within a time range
    ---
    parameters:
      - name: event_id
        in: path
        type: integer
        required: true
        description: Event ID to filter by
      - name: start_time
        in: path
        type: integer
        format: int64
        required: true
        description: Start timestamp in nanoseconds
      - name: end_time
        in: path
        type: integer
        format: int64
        required: true
        description: End timestamp in nanoseconds
    responses:
      200:
        description: Event with records within the specified time range
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Event ID
            name:
              type: string
              description: Event name
            records:
              type: array
              items:
                type: array
                items:
                  type: integer
                  format: int64
                  description: [timestamp in nanoseconds, data]
      404:
        description: Event not found
    """
    try:
        return jsonify({'error': "Coming soon..."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
