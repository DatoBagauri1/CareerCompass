import logging
from typing import Optional
import re

try:
    from langdetect import detect, DetectorFactory
    # Set seed for consistent results
    DetectorFactory.seed = 0
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

def detect_language(text: str) -> str:
    """
    Detect the language of the given text.
    Returns 'en' for English, 'ru' for Russian, 'ka' for Georgian, or 'en' as default.
    """
    if not text or not text.strip():
        return 'en'
    
    # Clean text for better detection
    clean_text = re.sub(r'[^\w\s]', ' ', text.lower().strip())
    
    if not LANGDETECT_AVAILABLE:
        # Fallback: Simple character-based detection
        return detect_language_fallback(clean_text)
    
    try:
        detected = detect(clean_text)
        
        # Map detected languages to supported ones
        if detected in ['en']:
            return 'en'
        elif detected in ['ru']:
            return 'ru'
        elif detected in ['ka']:
            return 'ka'
        else:
            # Check for language-specific patterns
            return detect_language_fallback(clean_text)
            
    except Exception as e:
        logging.warning(f"Language detection failed: {str(e)}")
        return detect_language_fallback(clean_text)

def detect_language_fallback(text: str) -> str:
    """
    Fallback language detection based on character patterns.
    """
    if not text:
        return 'en'
    
    # Count character types
    cyrillic_count = len(re.findall(r'[а-яё]', text, re.IGNORECASE))
    georgian_count = len(re.findall(r'[ა-ჰ]', text))
    latin_count = len(re.findall(r'[a-z]', text, re.IGNORECASE))
    
    total_chars = cyrillic_count + georgian_count + latin_count
    
    if total_chars == 0:
        return 'en'
    
    # Calculate percentages
    cyrillic_ratio = cyrillic_count / total_chars
    georgian_ratio = georgian_count / total_chars
    latin_ratio = latin_count / total_chars
    
    # Determine language based on character distribution
    if georgian_ratio > 0.1:  # Georgian has unique script
        return 'ka'
    elif cyrillic_ratio > 0.3:  # Strong Cyrillic presence
        return 'ru'
    elif latin_ratio > 0.5:  # Predominantly Latin
        return 'en'
    else:
        # Check for language-specific keywords
        return detect_by_keywords(text)

def detect_by_keywords(text: str) -> str:
    """
    Detect language based on common keywords.
    """
    text_lower = text.lower()
    
    # English keywords
    english_keywords = [
        'experience', 'education', 'skills', 'work', 'university', 'college',
        'project', 'software', 'developer', 'engineer', 'manager', 'analyst'
    ]
    
    # Russian keywords
    russian_keywords = [
        'опыт', 'образование', 'навыки', 'работа', 'университет', 'институт',
        'проект', 'разработчик', 'инженер', 'менеджер', 'аналитик', 'специалист'
    ]
    
    # Georgian keywords
    georgian_keywords = [
        'გამოცდილება', 'განათლება', 'უნარები', 'სამუშაო', 'უნივერსიტეტი',
        'პროექტი', 'დეველოპერი', 'ინჟინერი', 'მენეჯერი', 'ანალიტიკოსი'
    ]
    
    english_count = sum(1 for keyword in english_keywords if keyword in text_lower)
    russian_count = sum(1 for keyword in russian_keywords if keyword in text_lower)
    georgian_count = sum(1 for keyword in georgian_keywords if keyword in text_lower)
    
    if georgian_count > 0:
        return 'ka'
    elif russian_count > english_count:
        return 'ru'
    else:
        return 'en'

def get_language_name(lang_code: str) -> str:
    """
    Get human-readable language name from language code.
    """
    language_names = {
        'en': 'English',
        'ru': 'Russian',
        'ka': 'Georgian'
    }
    return language_names.get(lang_code, 'English')

def get_supported_languages() -> list:
    """
    Get list of supported language codes.
    """
    return ['en', 'ru', 'ka']