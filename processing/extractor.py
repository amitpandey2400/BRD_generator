"""
Information extraction engine using AI/NLP
Extracts requirements, decisions, timelines, and stakeholder feedback from text
"""
from typing import List, Dict, Optional
import json

from config.settings import settings
from utils.logger import get_logger
from utils.ai_client import ai_client

logger = get_logger(__name__)


class InformationExtractor:
    """Extract structured information from unstructured text"""
    
    def __init__(self):
        self.ai = ai_client
        
    async def extract_requirements(self, text: str, context: Optional[Dict] = None) -> List[Dict]:
        """
        Extract requirements from text
        
        Args:
            text: Input text
            context: Additional context (source type, project info, etc.)
            
        Returns:
            List of extracted requirements
        """
        prompt = f"""
You are an expert business analyst. Extract all requirements, features, and specifications from the following text.

For each requirement, provide:
1. Type: functional, non_functional, business, technical, or constraint
2. Title: Brief, clear title (max 100 characters)
3. Description: Detailed description of the requirement
4. Priority: High, Medium, or Low
5. Stakeholder: Who requested or benefits from this requirement
6. Acceptance Criteria: Specific, testable criteria (if mentioned)

Text to analyze:
{text}

Return ONLY a JSON array of requirements. Example format:
[
  {{
    "type": "functional",
    "title": "User Authentication",
    "description": "System must allow users to log in with email and password",
    "priority": "High",
    "stakeholder": "Security Team",
    "acceptance_criteria": "Users can successfully log in and out; Failed attempts show error message"
  }}
]
"""
        
        try:
            content = await self.ai.generate_completion(
                messages=[
                    {"role": "system", "content": "You are an expert business analyst who extracts requirements from text. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=settings.MAX_TOKENS
            )
            
            # Try to parse JSON from response
            requirements = json.loads(content)
            
            logger.info(f"Extracted {len(requirements)} requirements")
            return requirements
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse requirements JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Error extracting requirements: {e}")
            return []
    
    async def extract_decisions(self, text: str) -> List[Dict]:
        """Extract key decisions made in the text"""
        prompt = f"""
Extract all key decisions, resolutions, and agreements from the following text.

For each decision, provide:
1. Decision: What was decided
2. Context: Why this decision was made
3. Decided By: Who made the decision
4. Impact: Expected impact of this decision
5. Date: When it was decided (if mentioned)

Text:
{text}

Return ONLY a JSON array of decisions.
"""
        
        try:
            content = await self.ai.generate_completion(
                messages=[
                    {"role": "system", "content": "You are an expert at identifying key decisions in business communications. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            decisions = json.loads(content)
            
            logger.info(f"Extracted {len(decisions)} decisions")
            return decisions
            
        except Exception as e:
            logger.error(f"Error extracting decisions: {e}")
            return []
    
    async def extract_stakeholders(self, text: str) -> List[Dict]:
        """Extract stakeholder information"""
        prompt = f"""
Identify all stakeholders mentioned in the following text.

For each stakeholder, provide:
1. Name: Stakeholder name or role
2. Role: Their role or title
3. Interest: Their interest or concern in the project
4. Influence: Their level of influence (High, Medium, Low)
5. Contact: Email or contact info (if mentioned)

Text:
{text}

Return ONLY a JSON array of stakeholders.
"""
        
        try:
            content = await self.ai.generate_completion(
                messages=[
                    {"role": "system", "content": "You are an expert at identifying stakeholders. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            stakeholders = json.loads(content)
            
            logger.info(f"Extracted {len(stakeholders)} stakeholders")
            return stakeholders
            
        except Exception as e:
            logger.error(f"Error extracting stakeholders: {e}")
            return []
    
    async def extract_timeline(self, text: str) -> List[Dict]:
        """Extract timeline, milestones, and deadlines"""
        prompt = f"""
Extract all timeline information, milestones, deadlines, and dates from the following text.

For each timeline item, provide:
1. Event: What needs to happen
2. Date: When it should happen
3. Type: milestone, deadline, or event
4. Owner: Who is responsible (if mentioned)
5. Dependencies: What needs to be done first (if mentioned)

Text:
{text}

Return ONLY a JSON array of timeline items.
"""
        
        try:
            content = await self.ai.generate_completion(
                messages=[
                    {"role": "system", "content": "You are an expert at extracting timeline information. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            timeline = json.loads(content)
            
            logger.info(f"Extracted {len(timeline)} timeline items")
            return timeline
            
        except Exception as e:
            logger.error(f"Error extracting timeline: {e}")
            return []
    
    async def extract_assumptions(self, text: str) -> List[str]:
        """Extract assumptions and constraints"""
        prompt = f"""
Extract all assumptions, constraints, and limitations mentioned in the following text.

Return ONLY a JSON array of strings, each describing one assumption or constraint.

Text:
{text}
"""
        
        try:
            content = await self.ai.generate_completion(
                messages=[
                    {"role": "system", "content": "You are an expert at identifying assumptions and constraints. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            assumptions = json.loads(content)
            
            logger.info(f"Extracted {len(assumptions)} assumptions")
            return assumptions
            
        except Exception as e:
            logger.error(f"Error extracting assumptions: {e}")
            return []
    
    async def extract_success_metrics(self, text: str) -> List[Dict]:
        """Extract success metrics and KPIs"""
        prompt = f"""
Extract all success metrics, KPIs, and success criteria from the following text.

For each metric, provide:
1. Metric: Name of the metric
2. Description: What it measures
3. Target: Target value or goal (if mentioned)
4. Measurement Method: How it will be measured (if mentioned)

Text:
{text}

Return ONLY a JSON array of metrics.
"""
        
        try:
            content = await self.ai.generate_completion(
                messages=[
                    {"role": "system", "content": "You are an expert at identifying success metrics. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            metrics = json.loads(content)
            
            logger.info(f"Extracted {len(metrics)} success metrics")
            return metrics
            
        except Exception as e:
            logger.error(f"Error extracting success metrics: {e}")
            return []
