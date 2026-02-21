"""
Sentiment analysis for stakeholder communications
"""
from typing import Dict, List
from openai import AsyncOpenAI
import json

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class SentimentAnalyzer:
    """Analyze sentiment and extract concerns from stakeholder communications"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def analyze_sentiment(self, text: str, stakeholder: str = "Unknown") -> Dict:
        """
        Analyze sentiment of communication
        
        Args:
            text: Text to analyze
            stakeholder: Name/role of the stakeholder
            
        Returns:
            Dictionary with sentiment analysis results
        """
        prompt = f"""
Analyze the sentiment and tone of the following communication from {stakeholder}.

Provide:
1. Overall Sentiment: positive, negative, or neutral
2. Sentiment Score: -100 (very negative) to 100 (very positive)
3. Confidence Level: High, Medium, Low
4. Key Emotions: List of detected emotions
5. Concerns: List of any concerns or worries expressed
6. Positive Points: List of positive aspects mentioned
7. Tone: professional, casual, urgent, frustrated, enthusiastic, etc.

Text:
{text}

Return ONLY a JSON object with the analysis.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing sentiment and emotional tone in business communications. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            result['stakeholder'] = stakeholder
            
            logger.info(
                f"Sentiment analysis for {stakeholder}: "
                f"{result.get('sentiment')} ({result.get('sentiment_score')})"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                "sentiment": "neutral",
                "sentiment_score": 0,
                "confidence": "Low",
                "key_emotions": [],
                "concerns": [],
                "positive_points": [],
                "tone": "unknown",
                "stakeholder": stakeholder
            }
    
    async def extract_concerns(self, text: str) -> List[Dict]:
        """
        Extract specific concerns and issues from text
        
        Returns:
            List of concerns with details
        """
        prompt = f"""
Extract all concerns, issues, risks, or objections mentioned in the following text.

For each concern, provide:
1. Concern: Brief description of the concern
2. Category: technical, business, timeline, budget, resource, quality, or other
3. Severity: Critical, High, Medium, Low
4. Mentioned By: Who raised this concern (if identifiable)
5. Proposed Solution: Any solution mentioned (if any)

Text:
{text}

Return ONLY a JSON array of concerns.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at identifying concerns and risks. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            concerns = json.loads(content)
            
            logger.info(f"Extracted {len(concerns)} concerns")
            return concerns
            
        except Exception as e:
            logger.error(f"Error extracting concerns: {e}")
            return []
    
    async def summarize_stakeholder_feedback(
        self,
        texts: List[str],
        stakeholder: str
    ) -> Dict:
        """
        Summarize all feedback from a specific stakeholder
        
        Args:
            texts: List of communications from the stakeholder
            texts: Stakeholder name/role
            
        Returns:
            Summary of stakeholder's overall feedback and sentiment
        """
        combined_text = "\n\n---\n\n".join(texts[:10])  # Limit to recent messages
        
        prompt = f"""
Summarize all feedback and communications from {stakeholder}.

Provide:
1. Overall Summary: Key themes and messages
2. Main Requirements: Any requirements they've expressed
3. Primary Concerns: Their main concerns or objections
4. Support Level: How supportive they are (Very Supportive, Supportive, Neutral, Concerned, Opposed)
5. Engagement Level: How engaged they are (High, Medium, Low)
6. Action Items: Any action items they've mentioned or requested

Communications:
{combined_text}

Return ONLY a JSON object with the summary.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at summarizing stakeholder communications. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            result['stakeholder'] = stakeholder
            result['num_communications'] = len(texts)
            
            return result
            
        except Exception as e:
            logger.error(f"Error summarizing stakeholder feedback: {e}")
            return {
                "stakeholder": stakeholder,
                "overall_summary": "Error during analysis",
                "main_requirements": [],
                "primary_concerns": [],
                "support_level": "Unknown",
                "engagement_level": "Unknown",
                "action_items": [],
                "num_communications": len(texts)
            }
