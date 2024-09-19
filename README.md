# Zendesk - Tracking Pixel 

## Objective

This Python script is designed to provide your Support Team with valuable insights into when the requester (the individual who originally created the support ticket) opens the email containing the team's reply or solution. Every time the requester opens the email, the script will automatically trigger an action that adds an internal comment to the corresponding support ticket.

The key functionality of this script is its ability to track email opens in real time, allowing your support agents to monitor the recipient's engagement with their response. When the requester views the email, the script detects this event and creates an internal note within the ticket system. This internal comment is added to the ticket associated with the requester, providing your team with visibility into when the requester has engaged with the communication.

By using this tool, your support team can:
- Track whether and when the requester opens the email response.
- Gain insight into the timing of the requester's engagement with the support ticket.
- Improve follow-up decisions, as support agents will know whether the email has been seen, helping to prioritize tickets or anticipate further interaction.

The automatic logging of email opens within the ticket's internal comment section ensures that this data is easily accessible and well-organized for future reference.

## How does it work?

To implement this solution, follow the steps below to track when the requester opens an email, allowing the support team to see the exact time an email related to a ticket is opened. The process involves adding a tracking pixel to the email, setting up a Flask web server to detect when the pixel is loaded, and sending a notification back to Zendesk.

### Add a Tracking Pixel in the Zendesk Trigger
First, you need to modify the Zendesk trigger that sends a message to the requester when there’s an update on their support ticket. This involves embedding an HTML <img> tag in the email template, which inserts a 1x1 invisible tracking GIF into the message. The tracking pixel HTML code looks like this:

```
<img border="0" width="1" height="1" alt="track-pixel" title="track-pixel" style="display:block" src="http://XX.XX.XX.XX:5000/pixel.gif?ticket_id={{ticket.id}}">
```
- **`src` attribute:** Replace the `XX.XX.XX.XX` with the public IP address of your server (for example, an EC2 instance). This is where your Flask application will run, and it will listen for requests when the pixel is loaded. Make sure to replace the placeholder with the actual IP address of your instance.
- **`ticket_id` query parameter:** The `{{ticket.id}}` placeholder will dynamically insert the relevant ticket ID into the URL. This allows the script to link the email open event to the correct ticket in Zendesk.

> [!NOTE]
> Be aware that the public IP address of the server where the Flask app is hosted may change over time. You’ll need to update the IP in the HTML code if that happens or use a domain name for better reliability.

### Set Up a Flask Application
We use Flask, a micro web framework to detect when the tracking pixel (a 1x1 invisible GIF) is opened. Flask will handle HTTP requests for the image. When the user opens the email and the 1x1 GIF loads, Flask captures this event and logs it as the user opening the email. Here’s a brief outline of what happens in the background:

1. **Flask listens for requests:** When the requester opens the email, their email client loads the 1x1 invisible GIF from your server.
2. **Tracking the email open:** As the image is loaded, a GET request is sent to the server hosting the tracking pixel (Flask). The server knows which ticket was opened based on the `ticket_id` parameter in the request.
3. **Sending a notification to Zendesk:** The Flask app then sends an API request to Zendesk to update the corresponding support ticket with an internal comment that logs the time the email was opened.

### The Requester's Interaction

Once the Support Team sends an email with the embedded tracking pixel to the requester, you simply wait for the requester's interaction. When the requester opens the email, their email client will automatically load the 1x1 invisible GIF, which triggers the Flask server. 

Although the tracking pixel is invisible to the human eye, it serves as a beacon that signals the email has been opened. By loading this image, the Flask server is notified, and it can take further action, like updating the ticket in Zendesk.

### Logging the Email Open in Zendesk

Once the tracking pixel is loaded (i.e., when the requester opens the email), the Flask script captures this event and sends an API request to Zendesk. The API call adds an internal comment to the support ticket, notifying the support team that the email was opened. For example, the comment added could look like this:

![Screenshot 2024-09-19 at 13 03 39](https://github.com/user-attachments/assets/f58eb5e2-be5a-485e-87ba-3a43cb1e4ccb)

Where `{string_current_date_time}` is dynamically replaced with the exact date and time when the email was opened, which is also the moment the tracking pixel was loaded. This gives the support team real-time visibility into when the requester has engaged with the email, helping them track responsiveness and prioritize further actions. 

By following these steps, you’ll set up an email tracking mechanism that logs email opens as internal comments in Zendesk, using Flask to detect the loading of an invisible tracking pixel embedded in the email.

## Requisites

### Install Python
```
yum install python3
```
### Install pip
```
yum install python3-pip
```

### Install Flask
```
pip install flask
```
