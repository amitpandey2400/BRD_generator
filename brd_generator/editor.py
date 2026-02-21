"""
BRD Editor - Handles natural language editing of BRDs
"""
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from storage.models import BRD, BRDEdit
from config.settings import settings
from utils.logger import get_logger
from utils.ai_client import ai_client

logger = get_logger(__name__)


class BRDEditor:
    """Handle iterative editing of BRDs using natural language"""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.client = ai_client
    
    async def edit_brd(
        self,
        brd_id: str,
        edit_request: str,
        section: Optional[str] = None
    ) -> BRD:
        """
        Edit a BRD based on natural language request
        
        Args:
            brd_id: BRD ID to edit
            edit_request: Natural language edit request
            section: Optional specific section to edit
            
        Returns:
            Updated BRD
        """
        # Get BRD
        brd = await self.db.get(BRD, brd_id)
        if not brd:
            raise ValueError(f"BRD not found: {brd_id}")
        
        # Determine what to edit
        if section:
            section_to_edit = section
            current_content = getattr(brd, section, "")
        else:
            section_to_edit = await self._identify_section(edit_request, brd)
            current_content = getattr(brd, section_to_edit, "") if section_to_edit else brd.full_document
        
        # Generate edited content
        edited_content = await self._apply_edit(
            edit_request,
            current_content,
            section_to_edit
        )
        
        # Save edit history
        edit_record = BRDEdit(
            brd_id=brd_id,
            edit_request=edit_request,
            section_affected=section_to_edit,
            previous_content=current_content,
            new_content=edited_content
        )
        self.db.add(edit_record)
        
        # Update BRD
        if section_to_edit and hasattr(brd, section_to_edit):
            setattr(brd, section_to_edit, edited_content)
        
        # Regenerate full document
        brd.full_document = await self._regenerate_full_document(brd)
        brd.version += 1
        
        await self.db.commit()
        await self.db.refresh(brd)
        
        logger.info(f"Edited BRD {brd_id}: {section_to_edit}")
        
        return brd
    
    async def _identify_section(self, edit_request: str, brd: BRD) -> str:
        """Identify which section the edit request refers to"""
        prompt = f"""
Identify which section of the BRD this edit request refers to.

Edit Request: {edit_request}

Available Sections:
- executive_summary
- business_objectives
- stakeholder_analysis
- functional_requirements
- non_functional_requirements
- assumptions
- constraints
- success_metrics
- timeline
- risks

Return ONLY the section name (one of the options above). If it affects multiple sections or the entire document, return "full_document".
"""
        
        try:
            section_text = await self.client.generate_completion(
                system_message="You are an expert at understanding BRD edit requests.",
                user_message=prompt
            )
            
            section = section_text.strip()
            
            # Validate section name
            valid_sections = [
                'executive_summary', 'business_objectives', 'stakeholder_analysis',
                'functional_requirements', 'non_functional_requirements',
                'assumptions', 'constraints', 'success_metrics', 'timeline',
                'risks', 'full_document'
            ]
            
            if section not in valid_sections:
                return 'full_document'
            
            return section
            
        except Exception as e:
            logger.error(f"Error identifying section: {e}")
            return 'full_document'
    
    async def _apply_edit(
        self,
        edit_request: str,
        current_content: str,
        section: str
    ) -> str:
        """Apply the edit to the content"""
        prompt = f"""
You are editing the {section} section of a Business Requirements Document.

Current Content:
{current_content}

Edit Request:
{edit_request}

Generate the updated content that incorporates the requested changes while maintaining professional BRD formatting and quality.
Keep the structure and format consistent with the original unless specifically asked to change it.
"""
        
        try:
            edited_content = await self.client.generate_completion(
                system_message="You are an expert business analyst who edits BRDs with precision and professionalism.",
                user_message=prompt
            )
            return edited_content
            
        except Exception as e:
            logger.error(f"Error applying edit: {e}")
            return current_content
    
    async def _regenerate_full_document(self, brd: BRD) -> str:
        """Regenerate the full document with updated sections"""
        from datetime import datetime
        current_date = datetime.now().strftime("%B %d, %Y")
        
        document = f"""
# BUSINESS REQUIREMENTS DOCUMENT

## {brd.title}

**Date:** {current_date}
**Version:** {brd.version}

---

## 1. Executive Summary

{brd.executive_summary or 'To be completed'}

---

## 2. Business Objectives

{brd.business_objectives or 'To be completed'}

---

## 3. Stakeholder Analysis

{brd.stakeholder_analysis or 'To be completed'}

---

## 4. Functional Requirements

{brd.functional_requirements or 'To be completed'}

---

## 5. Non-Functional Requirements

{brd.non_functional_requirements or 'To be completed'}

---

## 6. Assumptions and Constraints

{brd.assumptions or 'To be completed'}

---

## 7. Success Metrics and KPIs

{brd.success_metrics or 'To be completed'}

---

## 8. Project Timeline and Milestones

{brd.timeline or 'To be completed'}

---

## 9. Risks and Mitigation Strategies

{brd.risks or 'To be completed'}

---

**Document Version History**

| Version | Date | Changes |
|---------|------|---------|
| {brd.version} | {current_date} | Updated via edit request |

"""
        
        return document
    
    async def get_edit_history(self, brd_id: str) -> list:
        """Get edit history for a BRD"""
        from sqlalchemy import select
        
        result = await self.db.execute(
            select(BRDEdit)
            .where(BRDEdit.brd_id == brd_id)
            .order_by(BRDEdit.created_at.desc())
        )
        
        edits = result.scalars().all()
        
        return [
            {
                'id': edit.id,
                'edit_request': edit.edit_request,
                'section_affected': edit.section_affected,
                'created_at': edit.created_at.isoformat()
            }
            for edit in edits
        ]
