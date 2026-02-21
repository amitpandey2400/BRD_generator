"""
BRD Generation using AI
Generates comprehensive Business Requirements Documents
"""
from typing import Dict, List, Optional
from datetime import datetime
import json

from config.settings import settings
from utils.logger import get_logger
from utils.ai_client import ai_client

logger = get_logger(__name__)


class BRDGenerator:
    """Generate structured Business Requirements Documents"""
    
    def __init__(self):
        self.client = ai_client
    
    async def generate_executive_summary(
        self,
        project_name: str,
        requirements: List[Dict],
        stakeholders: List[Dict],
        objectives: List[str]
    ) -> str:
        """Generate executive summary section"""
        prompt = f"""
Write a compelling executive summary for a Business Requirements Document.

Project: {project_name}

Business Objectives:
{chr(10).join([f"- {obj}" for obj in objectives]) if objectives else "- To be defined"}

Key Stakeholders:
{chr(10).join([f"- {s.get('name', 'Unknown')}: {s.get('role', 'N/A')}" for s in stakeholders[:5]])}

Total Requirements: {len(requirements)}

Write a 2-3 paragraph executive summary that:
1. Clearly states the project purpose and business value
2. Highlights key requirements and deliverables
3. Identifies main stakeholders and their interests
4. Sets expectations for project scope and outcomes

Make it concise, professional, and compelling for C-level executives.
"""
        
        return await self._generate_section(prompt)
    
    async def generate_business_objectives(
        self,
        project_context: str,
        extracted_objectives: List[str]
    ) -> str:
        """Generate business objectives section"""
        prompt = f"""
Create a comprehensive Business Objectives section.

Project Context:
{project_context}

Identified Objectives:
{chr(10).join([f"- {obj}" for obj in extracted_objectives]) if extracted_objectives else "- Objectives to be extracted from requirements"}

Generate a structured Business Objectives section that:
1. Lists primary and secondary objectives
2. Explains the business value and ROI potential
3. Aligns objectives with strategic business goals
4. Defines measurable outcomes

Format as clear, numbered objectives with descriptions.
"""
        
        return await self._generate_section(prompt)
    
    async def generate_stakeholder_analysis(
        self,
        stakeholders: List[Dict],
        sentiment_data: List[Dict]
    ) -> str:
        """Generate stakeholder analysis section"""
        stakeholder_info = []
        for sh in stakeholders:
            sentiment = next(
                (s for s in sentiment_data if s.get('stakeholder') == sh.get('name')),
                {}
            )
            
            stakeholder_info.append({
                'name': sh.get('name'),
                'role': sh.get('role'),
                'interest': sh.get('interest'),
                'influence': sh.get('influence'),
                'sentiment': sentiment.get('sentiment', 'unknown'),
                'concerns': sentiment.get('concerns', [])
            })
        
        prompt = f"""
Create a comprehensive Stakeholder Analysis section.

Stakeholders:
{json.dumps(stakeholder_info, indent=2)}

Generate a structured stakeholder analysis that:
1. Identifies all key stakeholders
2. Describes their roles and responsibilities
3. Assesses their level of influence and interest
4. Summarizes their concerns and feedback
5. Recommends engagement strategies

Format as a table or structured list with detailed descriptions.
"""
        
        return await self._generate_section(prompt)
    
    async def generate_functional_requirements(
        self,
        requirements: List[Dict]
    ) -> str:
        """Generate functional requirements section"""
        functional_reqs = [r for r in requirements if r.get('type') == 'functional']
        
        prompt = f"""
Create a comprehensive Functional Requirements section.

Requirements:
{json.dumps(functional_reqs, indent=2)}

Generate a structured functional requirements section that:
1. Groups requirements by feature or module
2. Provides clear, testable requirement statements
3. Includes acceptance criteria for each requirement
4. Indicates priority levels
5. References stakeholder sources

Use standard requirement numbering (FR-001, FR-002, etc.).
"""
        
        return await self._generate_section(prompt)
    
    async def generate_non_functional_requirements(
        self,
        requirements: List[Dict]
    ) -> str:
        """Generate non-functional requirements section"""
        non_functional_reqs = [
            r for r in requirements 
            if r.get('type') in ['non_functional', 'technical', 'constraint']
        ]
        
        prompt = f"""
Create a comprehensive Non-Functional Requirements section.

Requirements:
{json.dumps(non_functional_reqs, indent=2)}

Generate a structured non-functional requirements section covering:
1. Performance requirements
2. Security requirements
3. Scalability requirements
4. Reliability and availability
5. Usability requirements
6. Compliance and regulatory requirements
7. Technical constraints

Use standard requirement numbering (NFR-001, NFR-002, etc.).
"""
        
        return await self._generate_section(prompt)
    
    async def generate_assumptions_and_constraints(
        self,
        assumptions: List[str],
        constraints: List[str]
    ) -> str:
        """Generate assumptions and constraints section"""
        prompt = f"""
Create an Assumptions and Constraints section.

Assumptions:
{chr(10).join([f"- {a}" for a in assumptions]) if assumptions else "- None identified"}

Constraints:
{chr(10).join([f"- {c}" for c in constraints]) if constraints else "- None identified"}

Generate a structured section that:
1. Lists all project assumptions
2. Lists all constraints (technical, budget, timeline, resource)
3. Explains the impact of each
4. Identifies risks if assumptions prove incorrect

Format as two clear subsections with numbered items.
"""
        
        return await self._generate_section(prompt)
    
    async def generate_success_metrics(
        self,
        metrics: List[Dict],
        objectives: List[str]
    ) -> str:
        """Generate success metrics section"""
        prompt = f"""
Create a Success Metrics and KPIs section.

Identified Metrics:
{json.dumps(metrics, indent=2) if metrics else "No specific metrics identified"}

Business Objectives:
{chr(10).join([f"- {obj}" for obj in objectives])}

Generate a comprehensive success metrics section that:
1. Defines clear, measurable KPIs
2. Aligns metrics with business objectives
3. Specifies target values and thresholds
4. Describes measurement methods and frequency
5. Identifies data sources for each metric

Format as a structured list or table with detailed descriptions.
"""
        
        return await self._generate_section(prompt)
    
    async def generate_timeline(
        self,
        timeline_items: List[Dict]
    ) -> str:
        """Generate timeline and milestones section"""
        prompt = f"""
Create a Project Timeline and Milestones section.

Timeline Items:
{json.dumps(timeline_items, indent=2) if timeline_items else "Timeline to be defined during planning"}

Generate a comprehensive timeline section that:
1. Lists major milestones and deliverables
2. Indicates dependencies between phases
3. Identifies critical path items
4. Specifies responsible parties
5. Includes buffer time for risks

Format as a structured timeline or Gantt chart description.
"""
        
        return await self._generate_section(prompt)
    
    async def generate_full_document(
        self,
        project_name: str,
        sections: Dict[str, str]
    ) -> str:
        """Compile all sections into a complete BRD document"""
        current_date = datetime.now().strftime("%B %d, %Y")
        
        document = f"""
# BUSINESS REQUIREMENTS DOCUMENT

## {project_name}

**Date:** {current_date}
**Version:** 1.0

---

## Table of Contents

1. Executive Summary
2. Business Objectives
3. Stakeholder Analysis
4. Functional Requirements
5. Non-Functional Requirements
6. Assumptions and Constraints
7. Success Metrics and KPIs
8. Project Timeline and Milestones
9. Risks and Mitigation Strategies

---

## 1. Executive Summary

{sections.get('executive_summary', 'To be completed')}

---

## 2. Business Objectives

{sections.get('business_objectives', 'To be completed')}

---

## 3. Stakeholder Analysis

{sections.get('stakeholder_analysis', 'To be completed')}

---

## 4. Functional Requirements

{sections.get('functional_requirements', 'To be completed')}

---

## 5. Non-Functional Requirements

{sections.get('non_functional_requirements', 'To be completed')}

---

## 6. Assumptions and Constraints

{sections.get('assumptions_constraints', 'To be completed')}

---

## 7. Success Metrics and KPIs

{sections.get('success_metrics', 'To be completed')}

---

## 8. Project Timeline and Milestones

{sections.get('timeline', 'To be completed')}

---

## 9. Risks and Mitigation Strategies

{sections.get('risks', 'To be completed based on conflict analysis and stakeholder concerns')}

---

## Appendix

### A. Requirement Traceability Matrix
See separate document for detailed requirement traceability.

### B. Glossary
- **BRD**: Business Requirements Document
- **KPI**: Key Performance Indicator
- **NFR**: Non-Functional Requirement
- **FR**: Functional Requirement

### C. References
- Source communications and documents
- Stakeholder interview notes
- Meeting transcripts

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {current_date} | BRD Generator | Initial version |

"""
        
        return document
    
    async def _generate_section(self, prompt: str) -> str:
        """Helper method to generate a section using AI"""
        try:
            system_message = "You are an expert business analyst who writes clear, professional, and comprehensive business requirements documents."
            
            logger.info("Generating BRD section with AI...")
            content = await self.client.generate_completion(
                system_message=system_message,
                user_message=prompt
            )
            
            if content and len(content.strip()) > 0:
                logger.info(f"Successfully generated section ({len(content)} chars)")
                return content
            else:
                logger.warning("AI returned empty content")
                return "Content could not be generated. Please add more project data."
            
        except Exception as e:
            logger.error(f"Error generating section: {type(e).__name__} - {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return f"Unable to generate content at this time. Please ensure you have uploaded project documents or requirements."
