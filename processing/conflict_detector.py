"""
Conflict detection between requirements
"""
from typing import List, Dict, Tuple
from openai import AsyncOpenAI
import json

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class ConflictDetector:
    """Detect conflicts and contradictions between requirements"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def detect_conflicts(
        self,
        requirements: List[Dict]
    ) -> List[Dict]:
        """
        Detect conflicts between requirements
        
        Args:
            requirements: List of requirement dictionaries
            
        Returns:
            List of detected conflicts
        """
        if len(requirements) < 2:
            return []
        
        conflicts = []
        
        # Compare requirements in batches to avoid token limits
        batch_size = 10
        for i in range(0, len(requirements), batch_size):
            batch = requirements[i:i+batch_size]
            batch_conflicts = await self._analyze_requirement_batch(batch)
            conflicts.extend(batch_conflicts)
        
        logger.info(f"Detected {len(conflicts)} potential conflicts")
        return conflicts
    
    async def _analyze_requirement_batch(
        self,
        requirements: List[Dict]
    ) -> List[Dict]:
        """Analyze a batch of requirements for conflicts"""
        # Format requirements for analysis
        req_text = []
        for idx, req in enumerate(requirements):
            req_text.append(
                f"[REQ-{idx}] {req.get('title', 'Untitled')}: "
                f"{req.get('description', 'No description')}"
            )
        
        prompt = f"""
Analyze the following requirements for conflicts, contradictions, or incompatibilities.

Look for:
1. Direct contradictions (one requirement contradicts another)
2. Technical incompatibilities (requirements that can't coexist)
3. Resource conflicts (competing for same resources)
4. Priority conflicts (contradictory priorities)
5. Timeline conflicts (incompatible schedules)

Requirements:
{chr(10).join(req_text)}

For each conflict found, provide:
1. Requirement 1 ID: (e.g., REQ-0)
2. Requirement 2 ID: (e.g., REQ-3)
3. Conflict Type: contradiction, technical_incompatibility, resource_conflict, priority_conflict, or timeline_conflict
4. Description: Detailed explanation of the conflict
5. Severity: Critical, High, Medium, or Low
6. Suggested Resolution: How to resolve this conflict

Return ONLY a JSON array of conflicts. If no conflicts found, return an empty array [].
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at identifying conflicts between business requirements. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            conflicts = json.loads(content)
            
            # Map back to actual requirement IDs
            for conflict in conflicts:
                req1_idx = self._extract_req_index(conflict.get('requirement_1_id', ''))
                req2_idx = self._extract_req_index(conflict.get('requirement_2_id', ''))
                
                if req1_idx is not None and req2_idx is not None:
                    if req1_idx < len(requirements) and req2_idx < len(requirements):
                        conflict['requirement_1'] = requirements[req1_idx]
                        conflict['requirement_2'] = requirements[req2_idx]
            
            return conflicts
            
        except Exception as e:
            logger.error(f"Error detecting conflicts: {e}")
            return []
    
    def _extract_req_index(self, req_id: str) -> int:
        """Extract numeric index from requirement ID like 'REQ-0'"""
        try:
            return int(req_id.split('-')[1])
        except (IndexError, ValueError):
            return None
    
    async def check_requirement_compatibility(
        self,
        req1: Dict,
        req2: Dict
    ) -> Dict:
        """
        Check if two specific requirements are compatible
        
        Returns:
            Compatibility analysis result
        """
        prompt = f"""
Analyze the compatibility between these two requirements:

Requirement 1:
Title: {req1.get('title')}
Description: {req1.get('description')}
Type: {req1.get('type')}

Requirement 2:
Title: {req2.get('title')}
Description: {req2.get('description')}
Type: {req2.get('type')}

Determine:
1. Are they compatible? (yes/no/partial)
2. Compatibility Score: 0-100 (100 = fully compatible)
3. Issues: List any compatibility issues
4. Dependencies: Is one dependent on the other?
5. Recommendation: How to handle these requirements together

Return ONLY a JSON object with the analysis.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing requirement compatibility. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            return result
            
        except Exception as e:
            logger.error(f"Error checking compatibility: {e}")
            return {
                "compatible": "yes",
                "compatibility_score": 100,
                "issues": [],
                "dependencies": "none",
                "recommendation": "No conflicts detected"
            }
    
    async def suggest_conflict_resolution(
        self,
        conflict: Dict
    ) -> Dict:
        """
        Suggest resolutions for a specific conflict
        
        Args:
            conflict: Conflict dictionary
            
        Returns:
            Resolution suggestions
        """
        req1 = conflict.get('requirement_1', {})
        req2 = conflict.get('requirement_2', {})
        
        prompt = f"""
Suggest resolutions for this requirement conflict:

Conflict Description: {conflict.get('description')}
Severity: {conflict.get('severity')}

Requirement 1: {req1.get('title')} - {req1.get('description')}
Requirement 2: {req2.get('title')} - {req2.get('description')}

Provide multiple resolution options:
1. Resolution Option: Brief description
2. Pros: Benefits of this approach
3. Cons: Drawbacks of this approach
4. Implementation Effort: Low, Medium, High
5. Recommended: true/false (is this the recommended option?)

Return ONLY a JSON array of resolution options.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at resolving requirement conflicts. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            content = response.choices[0].message.content
            resolutions = json.loads(content)
            
            return {
                "conflict": conflict,
                "resolution_options": resolutions
            }
            
        except Exception as e:
            logger.error(f"Error suggesting resolutions: {e}")
            return {
                "conflict": conflict,
                "resolution_options": []
            }
