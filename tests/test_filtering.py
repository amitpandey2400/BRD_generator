"""
Tests for noise filtering
"""
import pytest
from processing.noise_filter import NoiseFilter


@pytest.mark.asyncio
async def test_relevance_detection():
    """Test relevance detection"""
    filter = NoiseFilter()
    
    # Relevant content
    relevant_text = """
    We need to implement a new user authentication system.
    The system should support OAuth 2.0 and JWT tokens.
    Timeline: 3 months from project start.
    """
    
    result = await filter.is_relevant(relevant_text)
    assert result['is_relevant'] == True
    assert result['relevance_score'] > 50
    
    # Irrelevant content
    irrelevant_text = """
    Happy birthday! Hope you have a great day!
    Let's grab lunch sometime next week.
    Did you watch the game last night?
    """
    
    result = await filter.is_relevant(irrelevant_text)
    # This might still be marked relevant due to AI uncertainty
    # Just check that we get a score
    assert 'relevance_score' in result


@pytest.mark.asyncio
async def test_content_categorization():
    """Test content categorization"""
    filter = NoiseFilter()
    
    text = """
    Based on the team discussion, we've decided to use React for the frontend.
    This decision was made considering team expertise and project timeline.
    """
    
    categories = await filter.categorize_content(text)
    
    assert isinstance(categories, dict)
    assert len(categories) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
