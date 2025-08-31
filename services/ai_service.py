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
            logger.info(f"AI Service: Generating {count} words for context '{context}', languages {language_from}->{language_to}")
            
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
        return f"""Generate {count} Dutch words with English translations for context: {context}. Level A1-A2. Return only JSON array:
[{{"word": "Dutch word", "translation": "English translation", "example_sentence_L1": "Dutch example", "example_sentence_L2": "English example"}}]"""

    def _create_russian_prompt(self, context: str, count: int) -> str:
        """Create prompt for English to Russian translation"""
        return f"""Generate {count} Russian words with English translations for context: {context}. Level A1-A2. Return only JSON array:
[{{"word": "Russian word", "translation": "English translation", "example_sentence_L1": "Russian example", "example_sentence_L2": "English example"}}]"""

    def _create_english_from_dutch_prompt(self, context: str, count: int) -> str:
        """Create prompt for Dutch to English translation"""
        return f"""Generate {count} English words with Dutch translations for context: {context}. Level A1-A2. Return only JSON array:
[{{"word": "English word", "translation": "Dutch translation", "example_sentence_L1": "English example", "example_sentence_L2": "Dutch example"}}]"""

    def _create_english_from_russian_prompt(self, context: str, count: int) -> str:
        """Create prompt for Russian to English translation"""
        return f"""Generate {count} English words with Russian translations for context: {context}. Level A1-A2. Return only JSON array:
[{{"word": "English word", "translation": "Russian translation", "example_sentence_L1": "English example", "example_sentence_L2": "Russian example"}}]"""

    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful language learning assistant. Always respond with valid JSON only. Do not include any explanations or markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content

    def _parse_word_list(self, response: str) -> List[Dict[str, str]]:
        """Parse OpenAI response into word list"""
        import json
        import re
        
        try:
            # Log the raw response for debugging
            logger.info(f"Raw OpenAI response length: {len(response)}")
            logger.info(f"Raw OpenAI response preview: {response[:200]}...")
            
            # Clean up response and parse JSON
            cleaned_response = response.strip()
            
            # Remove markdown code blocks
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            # Remove any leading/trailing whitespace
            cleaned_response = cleaned_response.strip()
            
            # Try to find JSON array in the response
            json_match = re.search(r'\[.*\]', cleaned_response, re.DOTALL)
            if json_match:
                cleaned_response = json_match.group(0)
            
            logger.info(f"Cleaned response preview: {cleaned_response[:200]}...")
            
            # Parse JSON
            words = json.loads(cleaned_response)
            
            # Validate structure
            if not isinstance(words, list):
                raise ValueError("Response is not a list")
            
            for word in words:
                if not all(key in word for key in ["word", "translation", "example_sentence_L1", "example_sentence_L2"]):
                    raise ValueError("Invalid word structure")
            
            logger.info(f"Successfully parsed {len(words)} words")
            return words
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response that failed to parse: {response}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error parsing response: {e}")
            return []
        except Exception as e:
            logger.error(f"Error parsing word list: {e}")
            return []

# Global instance
ai_service = AIService()
