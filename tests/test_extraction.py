"""
Tests for information extraction
"""
import pytest
from processing.extractor import InformationExtractor


@pytest.mark.asyncio
async def test_extract_requirements():
    """Test requirement extraction"""
    extractor = InformationExtractor()
    
    text = """
    The system must allow users to log in with email and password.
    Users should be able to reset their password via email.
    The application must support 10,000 concurrent users.
    Response time should be under 2 seconds for all operations.
    """
    
    requirements = await extractor.extract_requirements(text)
    
    assert len(requirements) > 0
    assert any(req['type'] == 'functional' for req in requirements)
    assert any(req['type'] == 'non_functional' for req in requirements)


@pytest.mark.asyncio
async def test_extract_decisions():
    """Test decision extraction"""
    extractor = InformationExtractor()
    
    text = """
    After discussing with the team, we decided to use PostgreSQL as our database.
    The CEO approved moving forward with the mobile-first approach.
    We agreed to postpone the API versioning feature until v2.0.
    """
    
    decisions = await extractor.extract_decisions(text)
    
    assert len(decisions) >= 2
    assert any('PostgreSQL' in str(d) or 'database' in str(d) for d in decisions)


@pytest.mark.asyncio
async def test_extract_stakeholders():
    """Test stakeholder extraction"""
    extractor = InformationExtractor()
    
    text = """
    John Smith, the CEO, emphasized the importance of user experience.
    Sarah Johnson from Marketing requested analytics dashboard.
    The IT Director expressed concerns about security.
    """
    
    stakeholders = await extractor.extract_stakeholders(text)
    
    assert len(stakeholders) > 0
    assert any('CEO' in str(s) for s in stakeholders)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
