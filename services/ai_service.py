import openai
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def generate_word_list(
        self, 
        context: str, 
        language_from: str, 
        language_to: str, 
        count: int = 20
    ) -> List[Dict[str, str]]:
        """
        Generate a custom word list based on context and language pair
        """
        try:
            # Validate count (max 100 words)
            if count > 100:
                count = 100
                logger.warning(f"Requested count {count} exceeds maximum, setting to 100")
            
            # Create prompt based on language pair
            if language_from == "en" and language_to == "nl":
                prompt = self._create_dutch_prompt(context, count)
            elif language_from == "en" and language_to == "ru":
                prompt = self._create_russian_prompt(context, count)
            elif language_from == "nl" and language_to == "en":
                prompt = self._create_english_from_dutch_prompt(context, count)
            elif language_from == "ru" and language_to == "en":
                prompt = self._create_english_from_russian_prompt(context, count)
            else:
                raise ValueError(f"Unsupported language pair: {language_from} -> {language_to}")
            
            # Call OpenAI API
            response = await self._call_openai(prompt)
            
            # Parse response
            words = self._parse_word_list(response)
            
            logger.info(f"Generated {len(words)} words for context: {context}")
            return words
            
        except Exception as e:
            logger.error(f"Error generating word list: {e}")
            return []
    
    def _create_dutch_prompt(self, context: str, count: int) -> str:
        """Create prompt for English to Dutch translation"""
        return f"""
Generate a list of {count} words in Dutch with translations into English.
Level: A1-A2.
Context: {context}.
Output JSON with fields: word, translation, example_sentence_L1, example_sentence_L2.

Format the response as a JSON array:
[
  {{
    "word": "Dutch word/phrase",
    "translation": "English translation",
    "example_sentence_L1": "Simple Dutch example sentence",
    "example_sentence_L2": "Simple English example sentence"
  }}
]

Focus on practical, everyday vocabulary at A1-A2 level that would be useful in this context.
Keep the words/phrases simple and commonly used.
"""

    def _create_russian_prompt(self, context: str, count: int) -> str:
        """Create prompt for English to Russian translation"""
        return f"""
Generate a list of {count} words in Russian with translations into English.
Level: A1-A2.
Context: {context}.
Output JSON with fields: word, translation, example_sentence_L1, example_sentence_L2.

Format the response as a JSON array:
[
  {{
    "word": "Russian word/phrase",
    "translation": "English translation", 
    "example_sentence_L1": "Simple Russian example sentence",
    "example_sentence_L2": "Simple English example sentence"
  }}
]

Focus on practical, everyday vocabulary at A1-A2 level that would be useful in this context.
Keep the words/phrases simple and commonly used.
"""

    def _create_english_from_dutch_prompt(self, context: str, count: int) -> str:
        """Create prompt for Dutch to English translation"""
        return f"""
Generate a list of {count} words in English with translations into Dutch.
Level: A1-A2.
Context: {context}.
Output JSON with fields: word, translation, example_sentence_L1, example_sentence_L2.

Format the response as a JSON array:
[
  {{
    "word": "English word/phrase",
    "translation": "Dutch translation",
    "example_sentence_L1": "Simple English example sentence",
    "example_sentence_L2": "Simple Dutch example sentence"
  }}
]

Focus on practical, everyday vocabulary at A1-A2 level that would be useful in this context.
Keep the words/phrases simple and commonly used.
"""

    def _create_english_from_russian_prompt(self, context: str, count: int) -> str:
        """Create prompt for Russian to English translation"""
        return f"""
Generate a list of {count} words in English with translations into Russian.
Level: A1-A2.
Context: {context}.
Output JSON with fields: word, translation, example_sentence_L1, example_sentence_L2.

Format the response as a JSON array:
[
  {{
    "word": "English word/phrase",
    "translation": "Russian translation",
    "example_sentence_L1": "Simple English example sentence",
    "example_sentence_L2": "Simple Russian example sentence"
  }}
]

Focus on practical, everyday vocabulary at A1-A2 level that would be useful in this context.
Keep the words/phrases simple and commonly used.
"""

    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful language learning assistant. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content

    def _parse_word_list(self, response: str) -> List[Dict[str, str]]:
        """Parse OpenAI response into word list"""
        import json
        try:
            # Clean up response and parse JSON
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            words = json.loads(cleaned_response)
            
            # Validate structure
            if not isinstance(words, list):
                raise ValueError("Response is not a list")
            
            for word in words:
                if not all(key in word for key in ["word", "translation", "example_sentence_L1", "example_sentence_L2"]):
                    raise ValueError("Invalid word structure")
            
            return words
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return []
        except Exception as e:
            logger.error(f"Error parsing word list: {e}")
            return []

# Global instance
ai_service = AIService()
