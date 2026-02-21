"""
Fireflies.ai API integration for meeting transcript ingestion
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class FirefliesClient:
    """Client for Fireflies.ai API integration"""
    
    BASE_URL = "https://api.fireflies.ai/graphql"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.FIREFLIES_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Execute a GraphQL query"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        try:
            response = requests.post(
                self.BASE_URL,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error executing Fireflies query: {e}")
            return {}
    
    def get_transcripts(
        self,
        limit: int = 50,
        days_back: int = 30
    ) -> List[Dict]:
        """
        Get recent meeting transcripts
        
        Args:
            limit: Maximum number of transcripts
            days_back: Number of days to look back
            
        Returns:
            List of transcript dictionaries
        """
        query = """
        query Transcripts($limit: Int!) {
            transcripts(limit: $limit) {
                id
                title
                date
                duration
                organizer_email
                participants
                meeting_url
                audio_url
                video_url
                transcript_url
                summary {
                    keywords
                    action_items
                    outline
                    shorthand_bullet
                    overview
                    bullet_gist
                }
                sentences {
                    text
                    speaker_name
                    speaker_id
                    start_time
                    end_time
                }
            }
        }
        """
        
        result = self._execute_query(query, {"limit": limit})
        transcripts = result.get('data', {}).get('transcripts', [])
        
        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days_back)
        filtered_transcripts = []
        
        for transcript in transcripts:
            try:
                transcript_date = datetime.fromisoformat(transcript['date'].replace('Z', '+00:00'))
                if transcript_date >= cutoff_date:
                    filtered_transcripts.append(transcript)
            except (ValueError, KeyError):
                continue
        
        logger.info(f"Retrieved {len(filtered_transcripts)} transcripts from Fireflies")
        return filtered_transcripts
    
    def get_transcript_by_id(self, transcript_id: str) -> Optional[Dict]:
        """Get a specific transcript by ID"""
        query = """
        query Transcript($id: String!) {
            transcript(id: $id) {
                id
                title
                date
                duration
                organizer_email
                participants
                meeting_url
                audio_url
                video_url
                transcript_url
                summary {
                    keywords
                    action_items
                    outline
                    shorthand_bullet
                    overview
                    bullet_gist
                }
                sentences {
                    text
                    speaker_name
                    speaker_id
                    start_time
                    end_time
                }
            }
        }
        """
        
        result = self._execute_query(query, {"id": transcript_id})
        return result.get('data', {}).get('transcript')
    
    def search_transcripts(
        self,
        keywords: List[str],
        limit: int = 50
    ) -> List[Dict]:
        """
        Search transcripts by keywords
        
        Args:
            keywords: List of keywords to search for
            limit: Maximum number of results
            
        Returns:
            List of matching transcripts
        """
        # Get all recent transcripts
        transcripts = self.get_transcripts(limit=limit)
        
        # Filter by keywords
        matching_transcripts = []
        for transcript in transcripts:
            # Check title
            title_match = any(
                keyword.lower() in transcript.get('title', '').lower()
                for keyword in keywords
            )
            
            # Check summary keywords
            summary_keywords = transcript.get('summary', {}).get('keywords', [])
            keyword_match = any(
                keyword.lower() in [sk.lower() for sk in summary_keywords]
                for keyword in keywords
            )
            
            # Check transcript text
            sentences = transcript.get('sentences', [])
            text_match = any(
                any(keyword.lower() in sentence.get('text', '').lower() for keyword in keywords)
                for sentence in sentences
            )
            
            if title_match or keyword_match or text_match:
                matching_transcripts.append(transcript)
        
        logger.info(f"Found {len(matching_transcripts)} transcripts matching keywords")
        return matching_transcripts
    
    def get_action_items(self, days_back: int = 30) -> List[Dict]:
        """
        Get all action items from recent meetings
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            List of action items with meeting context
        """
        transcripts = self.get_transcripts(days_back=days_back)
        
        action_items = []
        for transcript in transcripts:
            summary = transcript.get('summary', {})
            items = summary.get('action_items', [])
            
            for item in items:
                action_items.append({
                    'action_item': item,
                    'meeting_title': transcript.get('title'),
                    'meeting_date': transcript.get('date'),
                    'meeting_id': transcript.get('id'),
                    'organizer': transcript.get('organizer_email')
                })
        
        logger.info(f"Extracted {len(action_items)} action items from meetings")
        return action_items
    
    def get_transcript_text(self, transcript_id: str) -> str:
        """Get full transcript text"""
        transcript = self.get_transcript_by_id(transcript_id)
        if not transcript:
            return ""
        
        sentences = transcript.get('sentences', [])
        text_parts = []
        
        current_speaker = None
        for sentence in sentences:
            speaker = sentence.get('speaker_name', 'Unknown')
            text = sentence.get('text', '')
            
            if speaker != current_speaker:
                text_parts.append(f"\n{speaker}: {text}")
                current_speaker = speaker
            else:
                text_parts.append(text)
        
        return " ".join(text_parts)
