import firebase_admin
from firebase_admin import credentials, messaging
import os

# Initialize Firebase Admin SDK
cred_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'daini-project-firebase-adminsdk-fbsvc-1a12b008b7.json')
cred = credentials.Certificate(cred_path)

# Initialize the app if it hasn't been initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

def send_notification(title, body, token=None, topic=None):
    """
    Send a Firebase Cloud Message notification.
    
    Args:
        title (str): The notification title
        body (str): The notification body
        token (str, optional): The FCM registration token for a specific device
        topic (str, optional): The topic to send notification to
    
    Returns:
        dict: Response from FCM server
    """
    # Create message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
    )

    # Set target (either token or topic)
    if token:
        message.token = token
    elif topic:
        message.topic = topic
    else:
        raise ValueError("Either token or topic must be provided")

    try:
        # Send message
        response = messaging.send(message)
        return {"success": True, "message_id": response}
    except Exception as e:
        return {"success": False, "error": str(e)}
