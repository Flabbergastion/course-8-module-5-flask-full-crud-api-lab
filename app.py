from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Get JSON data from request
    data = request.get_json()
    
    # Validate that title is provided
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Generate new ID (find the highest existing ID and add 1)
    new_id = max([event.id for event in events], default=0) + 1
    
    # Create new event
    new_event = Event(new_id, data['title'])
    
    # Add to events list
    events.append(new_event)
    
    # Return the created event with 201 status
    return jsonify(new_event.to_dict()), 201

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Get JSON data from request
    data = request.get_json()
    
    # Validate that title is provided
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Find the event with the given ID
    for event in events:
        if event.id == event_id:
            # Update the event's title
            event.title = data['title']
            # Return the updated event
            return jsonify(event.to_dict()), 200
    
    # If event not found, return 404
    return jsonify({"error": "Event not found"}), 404

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find and remove the event with the given ID
    for i, event in enumerate(events):
        if event.id == event_id:
            # Remove the event from the list
            events.pop(i)
            # Return 204 No Content (successful deletion)
            return '', 204
    
    # If event not found, return 404
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
