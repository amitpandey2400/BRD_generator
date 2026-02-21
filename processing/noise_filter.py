"""
Intelligent noise filtering to identify project-relevant content
"""
from typing import Dict, Optional
from openai import AsyncOpenAI
import json

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class NoiseFilter:
    """Filter out irrelevant content and focus on project-related information"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def is_relevant(
        self,
        text: str,
        project_context: Optional[str] = None,
        keywords: Optional[list] = None
    ) -> Dict:
        """
        Determine if content is relevant to the project
        
        Args:
            text: Text content to analyze
            project_context: Optional context about the project
            keywords: Optional list of project keywords
            
        Returns:
            Dictionary with relevance info (is_relevant, score, reasoning)
        """
        context_part = f"\n\nProject Context: {project_context}" if project_context else ""
        keywords_part = f"\n\nProject Keywords: {', '.join(keywords)}" if keywords else ""
        
        prompt = f"""
Analyze the following text and determine if it contains information relevant to a business project or requirements gathering.

Relevant content includes:
- Requirements, features, or specifications
- Business decisions or approvals
- Stakeholder feedback or concerns
- Project timelines, milestones, or deadlines
- Technical constraints or assumptions
- Success criteria or metrics
- Budget or resource discussions
- Risk identification

Irrelevant content includes:
- Personal conversations unrelated to work
- Spam or automated messages
- Out-of-office replies
- Social pleasantries only
- Marketing content
- Unrelated announcements
{context_part}{keywords_part}

Text to analyze:
{text[:2000]}

Return ONLY a JSON object with this format:
{{
  "is_relevant": true/false,
  "relevance_score": 0-100,
  "reasoning": "Brief explanation of why this is or isn't relevant",
  "key_topics": ["topic1", "topic2"],
  "contains_requirements": true/false,
  "contains_decisions": true/false,
  "contains_stakeholder_feedback": true/false
}}
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at filtering business communications for project-relevant information. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            logger.info(
                f"Relevance analysis: {result['is_relevant']} "
                f"(score: {result['relevance_score']})"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing relevance: {e}")
            # Default to relevant to avoid losing data
            return {
                "is_relevant": True,
                "relevance_score": 50,
                "reasoning": "Error during analysis, defaulting to relevant",
                "key_topics": [],
                "contains_requirements": False,
                "contains_decisions": False,
                "contains_stakeholder_feedback": False
            }
    
    async def categorize_content(self, text: str) -> Dict:
        """
        Categorize content into types
        
        Returns:
            Dictionary with content categories and their confidence scores
        """
        prompt = f"""
Categorize the following business communication content.

Assign confidence scores (0-100) for each category:
1. Requirements Specification
2. Design Discussion
3. Technical Decision
4. Stakeholder Feedback
5. Timeline/Planning
6. Risk/Issue
7. Status Update
8. Question/Clarification
9. Approval/Sign-off
10. General Discussion

Text:
{text[:2000]}

Return ONLY a JSON object with category names as keys and confidence scores as values.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at categorizing business communications. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            categories = json.loads(content)
            
            return categories
            
        except Exception as e:
            logger.error(f"Error categorizing content: {e}")
            return {}
    
    async def extract_key_points(self, text: str, max_points: int = 5) -> list:
        """
        Extract key points from the text
        
        Args:
            text: Input text
            max_points: Maximum number of key points to extract
            
        Returns:
            List of key points
        """
        prompt = f"""
Extract the {max_points} most important key points from the following text.
Focus on actionable information, requirements, decisions, and critical details.

Text:
{text}

Return ONLY a JSON array of strings, each containing one key point.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at extracting key points from text. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            key_points = json.loads(content)
            
            return key_points
            
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return []
    
    async def deduplicate_content(self, texts: list[str]) -> list[int]:
        """
        Identify duplicate or highly similar content
        
        Args:
            texts: List of text contents
            
        Returns:
            List of indices to keep (duplicates removed)
        """
        if len(texts) <= 1:
            return list(range(len(texts)))
        
        # For now, return all indices
        # In production, use embeddings for semantic similarity
        return list(range(len(texts)))
