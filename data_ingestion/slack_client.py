"""
Slack API integration for message ingestion
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class SlackClient:
    """Client for Slack API integration"""
    
    def __init__(self, bot_token: Optional[str] = None):
        self.client = WebClient(token=bot_token or settings.SLACK_BOT_TOKEN)
        
    def get_channels(self) -> List[Dict]:
        """Get list of channels the bot has access to"""
        try:
            result = self.client.conversations_list(
                types="public_channel,private_channel"
            )
            channels = result.get('channels', [])
            logger.info(f"Retrieved {len(channels)} Slack channels")
            return channels
        except SlackApiError as e:
            logger.error(f"Error fetching Slack channels: {e}")
            return []
    
    def get_channel_messages(
        self,
        channel_id: str,
        days_back: int = 30,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get messages from a specific channel
        
        Args:
            channel_id: Slack channel ID
            days_back: Number of days to look back
            limit: Maximum number of messages
            
        Returns:
            List of message dictionaries
        """
        try:
            # Calculate oldest timestamp
            oldest = (datetime.now() - timedelta(days=days_back)).timestamp()
            
            result = self.client.conversations_history(
                channel=channel_id,
                oldest=str(oldest),
                limit=limit
            )
            
            messages = result.get('messages', [])
            logger.info(f"Retrieved {len(messages)} messages from channel {channel_id}")
            
            # Enrich messages with user info and thread replies
            enriched_messages = []
            for msg in messages:
                enriched_msg = self._enrich_message(msg, channel_id)
                enriched_messages.append(enriched_msg)
            
            return enriched_messages
            
        except SlackApiError as e:
            logger.error(f"Error fetching channel messages: {e}")
            return []
    
    def _enrich_message(self, message: Dict, channel_id: str) -> Dict:
        """Enrich message with user info and thread replies"""
        enriched = message.copy()
        
        # Get user info
        if 'user' in message:
            try:
                user_info = self.client.users_info(user=message['user'])
                enriched['user_name'] = user_info['user']['real_name']
                enriched['user_email'] = user_info['user'].get('profile', {}).get('email')
            except SlackApiError:
                pass
        
        # Get thread replies if message has them
        if message.get('thread_ts') and message.get('reply_count', 0) > 0:
            try:
                thread_result = self.client.conversations_replies(
                    channel=channel_id,
                    ts=message['thread_ts']
                )
                enriched['thread_replies'] = thread_result.get('messages', [])[1:]  # Exclude parent
            except SlackApiError:
                pass
        
        return enriched
    
    def search_messages(
        self,
        query: str,
        count: int = 100
    ) -> List[Dict]:
        """
        Search messages across all channels
        
        Args:
            query: Search query
            count: Maximum number of results
            
        Returns:
            List of matching messages
        """
        try:
            result = self.client.search_messages(
                query=query,
                count=count,
                sort='timestamp',
                sort_dir='desc'
            )
            
            matches = result.get('messages', {}).get('matches', [])
            logger.info(f"Found {len(matches)} messages matching '{query}'")
            return matches
            
        except SlackApiError as e:
            logger.error(f"Error searching Slack messages: {e}")
            return []
    
    def get_channel_info(self, channel_id: str) -> Optional[Dict]:
        """Get information about a specific channel"""
        try:
            result = self.client.conversations_info(channel=channel_id)
            return result.get('channel')
        except SlackApiError as e:
            logger.error(f"Error fetching channel info: {e}")
            return None
    
    def get_direct_messages(self, user_id: str, days_back: int = 30) -> List[Dict]:
        """Get direct messages with a specific user"""
        try:
            # Open DM channel
            dm_result = self.client.conversations_open(users=[user_id])
            channel_id = dm_result['channel']['id']
            
            # Get messages
            return self.get_channel_messages(channel_id, days_back=days_back)
            
        except SlackApiError as e:
            logger.error(f"Error fetching DMs: {e}")
            return []
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Find a user by their email address"""
        try:
            result = self.client.users_lookupByEmail(email=email)
            return result.get('user')
        except SlackApiError as e:
            logger.error(f"Error looking up user by email: {e}")
            return None
    
    def get_messages_by_keywords(
        self,
        keywords: List[str],
        channels: Optional[List[str]] = None,
        days_back: int = 30
    ) -> List[Dict]:
        """
        Get messages containing specific keywords
        
        Args:
            keywords: List of keywords to search for
            channels: Optional list of channel IDs to search in
            days_back: Number of days to look back
            
        Returns:
            List of matching messages
        """
        all_messages = []
        
        # Build search query
        query_parts = []
        for keyword in keywords:
            query_parts.append(f'"{keyword}"')
        query = " OR ".join(query_parts)
        
        # Add date filter
        after_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        query += f" after:{after_date}"
        
        # Search
        messages = self.search_messages(query)
        
        # Filter by channels if specified
        if channels:
            messages = [m for m in messages if m.get('channel', {}).get('id') in channels]
        
        return messages
