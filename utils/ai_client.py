"""
Unified AI Client for OpenAI and Google Gemini
Provides a single interface for different AI providers
"""
import google.generativeai as genai
from openai import AsyncOpenAI
from config.settings import settings
from typing import List, Dict, Any


class AIClient:
    """Unified AI client supporting both OpenAI and Gemini"""
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER.lower()
        
        if self.provider == "gemini":
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not set in environment")
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = settings.GEMINI_MODEL
        elif self.provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set in environment")
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
        else:
            raise ValueError(f"Unknown AI provider: {self.provider}")
    
    async def generate_completion(
        self, 
        messages: List[Dict[str, str]] = None,
        system_message: str = None,
        user_message: str = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Generate completion using configured AI provider
        
        Args:
            messages: List of message dicts with 'role' and 'content' (optional if system_message and user_message provided)
            system_message: System message/instructions (alternative to messages)
            user_message: User message/prompt (alternative to messages)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        # If system_message and user_message are provided, convert to messages format
        if messages is None:
            if system_message and user_message:
                messages = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ]
            elif user_message:
                messages = [{"role": "user", "content": user_message}]
            else:
                raise ValueError("Either messages or user_message must be provided")
        
        temperature = temperature or settings.TEMPERATURE
        max_tokens = max_tokens or settings.MAX_TOKENS
        
        if self.provider == "gemini":
            return await self._generate_gemini(messages, temperature, max_tokens)
        else:
            return await self._generate_openai(messages, temperature, max_tokens)
    
    async def _generate_gemini(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate completion using Google Gemini"""
        # Convert OpenAI-style messages to Gemini format
        prompt = self._messages_to_prompt(messages)
        
        model = genai.GenerativeModel(
            self.model,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
        )
        
        response = model.generate_content(prompt)
        return response.text
    
    async def _generate_openai(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate completion using OpenAI"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to a single prompt for Gemini"""
        prompt_parts = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                prompt_parts.append(f"Instructions: {content}\n")
            elif role == "user":
                prompt_parts.append(f"User: {content}\n")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}\n")
        
        return "\n".join(prompt_parts)


# Global instance
ai_client = AIClient()
