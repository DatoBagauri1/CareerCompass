import re
import logging
from typing import Dict, List, Any
from collections import Counter

# Technical skills by language
TECHNICAL_SKILLS = {
    'en': [
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
    'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'sass', 'less',
    
    # Frameworks and Libraries
    'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel',
    'rails', 'asp.net', '.net', 'jquery', 'bootstrap', 'tailwind', 'material-ui',
    
    # Databases
    'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite',
    'cassandra', 'dynamodb', 'neo4j',
    
    # Cloud and DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
    'terraform', 'ansible', 'puppet', 'chef', 'vagrant', 'nginx', 'apache',
    
    # Data Science and AI
    'machine learning', 'deep learning', 'artificial intelligence', 'data science',
    'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'opencv',
    'nlp', 'computer vision', 'statistics', 'analytics',
    
    # Tools and Platforms
    'jira', 'confluence', 'slack', 'teams', 'figma', 'sketch', 'photoshop', 'illustrator',
    'excel', 'powerpoint', 'tableau', 'power bi', 'splunk', 'datadog', 'new relic',
    
    # Methodologies
        'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd', 'microservices',
        'rest api', 'graphql', 'soap', 'oauth', 'jwt', 'mvp', 'mvc'
    ],
    'ru': [
        # Programming Languages (Russian)
        'питон', 'джава', 'джаваскрипт', 'typescript', 'с++', 'с#', 'пхп', 'руби', 'го', 'раст',
        'свифт', 'котлин', 'скала', 'эр', 'матлаб', 'эскьюэл', 'хтмл', 'цсс',
        
        # Frameworks and Libraries (Russian)
        'реакт', 'ангуляр', 'вью', 'node.js', 'экспресс', 'джанго', 'фласк', 'спринг', 'ларавел',
        'рейлс', 'asp.net', '.net', 'джейквери', 'бутстрап', 'тейлвинд',
        
        # Databases (Russian)
        'майэскьюэл', 'постгресэскьюэл', 'монгодб', 'редис', 'эластиксерч', 'оракл', 'эсэкэлайт',
        
        # Cloud and DevOps (Russian)
        'авс', 'азуре', 'гсп', 'докер', 'кубернетес', 'дженкинс', 'гит', 'гитхаб', 'гитлаб',
        'террафом', 'ансибл', 'паппет', 'чеф', 'вагрант', 'нжинкс', 'апач',
        
        # Data Science and AI (Russian)
        'машинное обучение', 'глубокое обучение', 'искусственный интеллект', 'наука о данных',
        'пандас', 'нампи', 'сайкит-лерн', 'тензорфлоу', 'пайторч', 'керас',
        'компьютерное зрение', 'статистика', 'аналитика',
        
        # Methodologies (Russian)
        'аджайл', 'скрам', 'канбан', 'девопс', 'непрерывная интеграция', 'микросервисы',
        'рест апи', 'графэкьюэл', 'соап', 'оаут', 'жвт'
    ],
    'ka': [
        # Programming Languages (Georgian)
        'პითონი', 'ჯავა', 'ჯავასკრიპტი', 'ტაიპსკრიპტი', 'სი++', 'სი#', 'პი-ჰ-პი', 'რუბი',
        'სვიფტი', 'კოტლინი', 'სკალა', 'ჰ-ტ-მ-ლ', 'ც-ს-ს',
        
        # Frameworks (Georgian)
        'რეაქტი', 'ანგულარი', 'ვიუ', 'ნოუდ.ჯს', 'ექსპრესი', 'ჯანგო', 'ფლასკი',
        'სპრინგი', 'ლარაველი', 'რეილსი',
        
        # Databases (Georgian)
        'მაისქლი', 'პოსტგრესქლი', 'მონგოდბ', 'რედისი',
        
        # Cloud and DevOps (Georgian)
        'ეიდაბლიუსი', 'აზურე', 'დოკერი', 'კუბერნეტესი', 'ჯენკინსი', 'გითი', 'გითჰაბი',
        
        # Data Science (Georgian)
        'მანქანური სწავლება', 'ღრმა სწავლება', 'ხელოვნური ინტელექტი', 'მონაცემთა მეცნიერება',
        'სტატისტიკა', 'ანალიტიკა',
        
        # Methodologies (Georgian)
        'აჯაილი', 'სკრამი', 'კანბანი', 'დევოფსი', 'მიკროსერვისები'
    ]
}

# Soft skills by language
SOFT_SKILLS = {
    'en': [
        'leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
        'creative', 'innovative', 'adaptable', 'flexible', 'organized', 'detail-oriented',
        'time management', 'project management', 'collaboration', 'mentoring',
        'customer service', 'presentation', 'negotiation', 'strategic thinking'
    ],
    'ru': [
        'лидерство', 'коммуникация', 'командная работа', 'решение проблем', 'аналитический',
        'креативный', 'инновационный', 'адаптивный', 'гибкий', 'организованный',
        'внимание к деталям', 'управление временем', 'управление проектами', 'сотрудничество',
        'менторство', 'обслуживание клиентов', 'презентация', 'переговоры', 'стратегическое мышление'
    ],
    'ka': [
        'ლიდერობა', 'კომუნიკაცია', 'გუნდური მუშაობა', 'პრობლემების გადაწყვეტა', 'ანალიტიკური',
        'კრეატიული', 'ინოვაციური', 'ადაპტირებადი', 'მოქნილი', 'ორგანიზებული',
        'დეტალებზე ყურადღება', 'დროის მართვა', 'პროექტის მართვა', 'თანამშრომლობა',
        'მენტორინგი', 'მომხმარებელთა სერვისი', 'პრეზენტაცია', 'მოლაპარაკება', 'სტრატეგიული აზროვნება'
    ]
}

def clean_text(text: str) -> str:
    """Clean and normalize text for analysis."""
    # Convert to lowercase and remove extra whitespace
    text = re.sub(r'\s+', ' ', text.lower().strip())
    # Remove special characters but keep alphanumeric and spaces
    text = re.sub(r'[^\w\s.-]', ' ', text)
    return text

def extract_skills(text: str, language: str = 'en') -> Dict[str, List[str]]:
    """Extract technical and soft skills from text."""
    clean_content = clean_text(text)
    
    found_technical = []
    found_soft = []
    
    # Get skills for the detected language, fallback to English
    tech_skills = TECHNICAL_SKILLS.get(language, TECHNICAL_SKILLS['en'])
    soft_skills = SOFT_SKILLS.get(language, SOFT_SKILLS['en'])
    
    # Also include English skills for broader matching
    if language != 'en':
        tech_skills.extend(TECHNICAL_SKILLS['en'])
        soft_skills.extend(SOFT_SKILLS['en'])
    
    # Find technical skills
    for skill in tech_skills:
        if skill.lower() in clean_content:
            found_technical.append(skill.title())
    
    # Find soft skills
    for skill in soft_skills:
        if skill.lower() in clean_content:
            found_soft.append(skill.title())
    
    # Remove duplicates while preserving order
    found_technical = list(dict.fromkeys(found_technical))
    found_soft = list(dict.fromkeys(found_soft))
    
    return {
        'technical': found_technical[:15],  # Limit to top 15
        'soft': found_soft[:10]  # Limit to top 10
    }

def calculate_ats_score(resume_text: str, job_description: str = "", language: str = 'en') -> Dict[str, Any]:
    """Calculate ATS score based on keyword matching."""
    if not resume_text.strip():
        return {
            'score': 0,
            'total_keywords': 0,
            'matched_keywords': [],
            'missing_keywords': []
        }
    
    resume_clean = clean_text(resume_text)
    
    if job_description.strip():
        # Extract keywords from job description
        job_clean = clean_text(job_description)
        job_words = set(word for word in job_clean.split() if len(word) > 2)
        
        # Get skills for language
        tech_skills = TECHNICAL_SKILLS.get(language, TECHNICAL_SKILLS['en'])
        soft_skills = SOFT_SKILLS.get(language, SOFT_SKILLS['en'])
        all_skills = tech_skills + soft_skills
        
        # Find technical terms in job description
        job_keywords = []
        for skill in all_skills:
            if skill.lower() in job_clean:
                job_keywords.append(skill)
        
        # Add other important words from job description
        common_job_words = [word for word in job_words if len(word) > 4]
        job_keywords.extend(common_job_words[:20])  # Add top 20 words
        
        # Remove duplicates
        job_keywords = list(set(job_keywords))
    else:
        # Use common industry keywords if no job description
        tech_skills = TECHNICAL_SKILLS.get(language, TECHNICAL_SKILLS['en'])
        soft_skills = SOFT_SKILLS.get(language, SOFT_SKILLS['en'])
        job_keywords = tech_skills[:30] + soft_skills[:15]
    
    # Count matches
    matched = []
    missing = []
    
    for keyword in job_keywords:
        if keyword.lower() in resume_clean:
            matched.append(keyword.title())
        else:
            missing.append(keyword.title())
    
    # Calculate score
    total_keywords = len(job_keywords)
    matched_count = len(matched)
    score = (matched_count / total_keywords * 100) if total_keywords > 0 else 0
    
    return {
        'score': round(score, 1),
        'total_keywords': total_keywords,
        'matched_keywords': matched[:20],  # Limit display
        'missing_keywords': missing[:15]   # Limit display
    }

def generate_suggestions(skills: Dict[str, List[str]], missing_keywords: List[str], language: str = 'en') -> List[str]:
    """Generate LinkedIn headline suggestions."""
    technical_skills = skills.get('technical', [])
    soft_skills = skills.get('soft', [])
    
    suggestions = []
    
    # Top technical skills for headlines
    top_tech = technical_skills[:3]
    top_soft = soft_skills[:2]
    
    if top_tech:
        # Tech-focused headline
        tech_str = " | ".join(top_tech)
        suggestions.append(f"Experienced {tech_str} Developer | Building Scalable Solutions")
        
        # Skills-focused headline
        if len(top_tech) >= 2:
            suggestions.append(f"{top_tech[0]} & {top_tech[1]} Specialist | Full-Stack Developer")
        
        # Leadership-focused headline
        if 'leadership' in [s.lower() for s in soft_skills]:
            suggestions.append(f"Tech Lead | {tech_str} Expert | Team Builder")
        else:
            suggestions.append(f"Senior Developer | {tech_str} | Problem Solver")
    else:
        # Generic suggestions when no tech skills found
        suggestions.extend([
            "Experienced Professional | Problem Solver | Team Player",
            "Results-Driven Specialist | Innovation Focused | Growth Minded",
            "Dedicated Professional | Strategic Thinker | Collaborative Leader"
        ])
    
    return suggestions[:3]

def analyze_resume(resume_text: str, job_description: str = "", language: str = 'en') -> Dict[str, Any]:
    """Main function to analyze resume and return comprehensive results."""
    try:
        if not resume_text.strip():
            return {
                'ats_score': 0.0,
                'skills': {'technical': [], 'soft': []},
                'missing_keywords': [],
                'suggestions': ["Please provide a resume with readable text content."]
            }
        
        # Extract skills
        skills = extract_skills(resume_text, language)
        
        # Calculate ATS score
        ats_result = calculate_ats_score(resume_text, job_description, language)
        
        # Generate suggestions
        suggestions = generate_suggestions(skills, ats_result['missing_keywords'], language)
        
        return {
            'ats_score': float(ats_result['score']),
            'skills': skills,
            'missing_keywords': list(ats_result['missing_keywords']),
            'matched_keywords': list(ats_result['matched_keywords']),
            'suggestions': list(suggestions),
            'total_keywords': int(ats_result['total_keywords'])
        }
        
    except Exception as e:
        logging.error(f"Error analyzing resume: {str(e)}")
        return {
            'ats_score': 0.0,
            'skills': {'technical': [], 'soft': []},
            'missing_keywords': [],
            'suggestions': ["Error analyzing resume. Please try again."]
        }
