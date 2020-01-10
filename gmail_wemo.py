#!/usr/bin/python3

import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pywemo

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    print("Authenticating credentials...")
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service
    
def choose_label(service):
    results = service.users().labels().list(userId='me').execute()
    labels = results['labels']
    print("Listing available labels...\n")
    for label in labels:
        print(label['name'])
    choice = input("\nSelect label to monitor: ")
    for label in labels:
        if choice.lower() == label['name'].lower():
            return label
    exit("No such label is available.")
    
def choose_device():
    print("Discovering WeMo devices...\n")
    devices = pywemo.discover_devices()
    if len(devices) == 0:
        exit("No WeMo devices found.")
    for device in devices:
        print(device.name)
    choice = input("\nChoose your device: ")
    
    for device in devices:
        if choice.lower() == device.name.lower():
            return device
    exit("No such device is available.")

def watch_label(service, label, device):
    print(f"Watching '{label['name']}' and controlling '{device.name}'...")
    if device.get_state() == 1:
        on = True
    else:
        on = False
    
    while True: 
        results = service.users().labels().get(userId='me', id=label['id']).execute()
        unread = results['messagesUnread']
        if unread == 0:
            if on:
                device.off()
                on = False
        else:
            if not on:
                device.on()
                on = True
        time.sleep(1)

if __name__ == '__main__':
    service = authenticate()
    label_id = choose_label(service)
    device = choose_device()
    watch_label(service, label_id, device)