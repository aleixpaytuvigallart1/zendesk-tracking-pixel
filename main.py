# import libraries
from flask import Flask, request, send_file
from datetime import datetime
import json
import requests
import os
import logging
import urllib3

urllib3.disable_warnings() # disable SSL warning messages

# Initialize Flask app
app = Flask(__name__)
print(os.environ)

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Route for pixel tracking
@app.route("/pixel.gif")

def send_api_request():
    
    # get current datetime and convert to string
    current_date_time = datetime.now()
    string_current_date_time = current_date_time.strftime("%d/%m/%Y, %H:%M:%S")
    
    # variables with ticket's data
    ticket_id = request.args.get('ticket_id')  # ticket ID 

    # if there is not a value in ticket_id, return error message and finish the function. Otherwise display logging.info
    if not ticket_id:
        logging.warning('No ticket_id found in the request')
        return '', 400  # Bad Request
    
    logging.info(f'Received request for ticket_id: {ticket_id}')
    
    # body of the message
    body = f'User has opened the ticket email at {string_current_date_time}'
    data = {'ticket': {'comment': {'body': body, 'public': False}}}
    
    # Set the request parameters
    user_email = os.getenv('ZENDESK_EMAIL')  # fetch from environment variable
    api_token = os.getenv('ZENDESK_API_TOKEN')  # fetch from environment variable
    domain = os.getenv('ZENDESK_DOMAIN') # fetch from environment variable 
    url = f'https://{domain}.zendesk.com/api/v2/tickets/{ticket_id}.json'

    # if there isn't any value in any of those 3 environment variables, return error message and finish the function. Otherwise move on
    if not user_email or not api_token or not domain:
        logging.error("Zendesk email or API token not configured in environment")
        return '', 500  # Internal Server Error
    
    # Authentication tuple
    auth = (f'{user_email}/token', api_token)  

    try:
        # Perform the HTTP PUT request to update the ticket
        response = requests.put(url, data=json.dumps(data), auth=auth, headers={'Content-Type': 'application/json'}, verify=False)
        
        # Log success or error based on response
        if response.status_code == 200:
            logging.info(f'Successfully updated ticket {ticket_id}')
        else:
            logging.error(f'Failed to update ticket {ticket_id}, status code: {response.status_code}, response: {response.text}')
        
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while updating ticket {ticket_id}: {e}")
        return '', 500  # Internal Server Error

    # Return a 1x1 transparent GIF
    return send_file('pixel.gif', mimetype='image/gif')

if __name__ == '__main__':
    # Use environment variables for sensitive info
    app.run(debug=True, host='0.0.0.0', port=5000)