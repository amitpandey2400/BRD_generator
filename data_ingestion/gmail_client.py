"""
Gmail API integration for email ingestion
"""
import os
import pickle
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import email
from email.mime.text import MIMEText

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailClient:
    """Client for Gmail API integration"""
    
    def __init__(self):
        self.creds = None
        self.service = None
        
    def authenticate(self, credentials_path: str = "credentials.json"):
        """Authenticate with Gmail API"""
        token_path = "token.pickle"
        
        # Load existing credentials
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('gmail', 'v1', credentials=self.creds)
        logger.info("Gmail API authenticated successfully")
        
    def get_messages(
        self,
        query: Optional[str] = None,
        max_results: int = 100,
        days_back: int = 30
    ) -> List[Dict]:
        """
        Retrieve messages from Gmail
        
        Args:
            query: Gmail search query (e.g., 'subject:project OR from:manager@company.com')
            max_results: Maximum number of messages to retrieve
            days_back: Number of days to look back
            
        Returns:
            List of message dictionaries
        """
        if not self.service:
            raise ValueError("Not authenticated. Call authenticate() first.")
        
        # Build query with date filter
        date_filter = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
        full_query = f"after:{date_filter}"
        if query:
            full_query += f" {query}"
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=full_query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            logger.info(f"Retrieved {len(messages)} messages from Gmail")
            
            # Fetch full message details
            detailed_messages = []
            for msg in messages:
                msg_detail = self._get_message_detail(msg['id'])
                if msg_detail:
                    detailed_messages.append(msg_detail)
            
            return detailed_messages
            
        except Exception as e:
            logger.error(f"Error retrieving Gmail messages: {e}")
            return []
    
    def _get_message_detail(self, message_id: str) -> Optional[Dict]:
        """Get detailed information for a specific message"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = message.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extract body
            body = self._extract_body(message.get('payload', {}))
            
            return {
                'id': message_id,
                'thread_id': message.get('threadId'),
                'subject': subject,
                'from': sender,
                'date': date,
                'body': body,
                'snippet': message.get('snippet', ''),
                'labels': message.get('labelIds', [])
            }
            
        except Exception as e:
            logger.error(f"Error getting message detail: {e}")
            return None
    
    def _extract_body(self, payload: Dict) -> str:
        """Extract message body from payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
                elif 'parts' in part:
                    body = self._extract_body(part)
                    if body:
                        break
        else:
            data = payload.get('body', {}).get('data', '')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body
    
    def search_by_keywords(self, keywords: List[str], days_back: int = 30) -> List[Dict]:
        """
        Search emails by keywords
        
        Args:
            keywords: List of keywords to search for
            days_back: Number of days to look back
            
        Returns:
            List of matching messages
        """
        # Build query with keywords
        query = " OR ".join([f"({keyword})" for keyword in keywords])
        return self.get_messages(query=query, days_back=days_back)
    
    def get_thread(self, thread_id: str) -> List[Dict]:
        """Get all messages in a thread"""
        try:
            thread = self.service.users().threads().get(
                userId='me',
                id=thread_id
            ).execute()
            
            messages = []
            for message in thread.get('messages', []):
                msg_detail = self._get_message_detail(message['id'])
                if msg_detail:
                    messages.append(msg_detail)
            
            return messages
            
        except Exception as e:
            logger.error(f"Error getting thread: {e}")
            return []
