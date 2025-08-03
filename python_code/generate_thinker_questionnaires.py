import os
import openai
from pathlib import Path
import argparse
from datetime import datetime
import json

def setup_openai_client(api_key=None):
    """Setup OpenAI client with API key."""
    if api_key:
        client = openai.OpenAI(api_key=api_key)
    else:
        # Try to get from environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable or pass it as argument.")
        client = openai.OpenAI(api_key=api_key)
    return client

def get_standard_questionnaire_examples():
    """
    Return example questionnaire structures to use as templates.
    These are common meaning questionnaire formats.
    """
    examples = {
        "MLQ": {
            "name": "Meaning in Life Questionnaire (MLQ)",
            "structure": """
            The Meaning in Life Questionnaire typically includes:
            
            1. PRESENCE OF MEANING (5 items) - measuring how much respondents feel their lives have meaning
            Example items:
            - I understand my life's meaning
            - My life has a clear sense of purpose
            - I have a good sense of what makes my life meaningful
            
            2. SEARCH FOR MEANING (5 items) - measuring how much respondents are actively seeking meaning
            Example items:
            - I am looking for something that makes my life feel meaningful
            - I am seeking a purpose or mission for my life
            - I am always looking to find my life's purpose
            
            Response scale: 1 (Absolutely untrue) to 7 (Absolutely true)
            """,
        },
        "PIL": {
            "name": "Purpose in Life Test (PIL)",
            "structure": """
            The Purpose in Life Test typically includes:
            
            Multiple dimensions of meaning:
            1. LIFE SATISFACTION AND EXCITEMENT
            2. GOAL-DIRECTEDNESS
            3. DEATH ACCEPTANCE
            4. FREEDOM
            5. SELF-REALIZATION
            6. MEANINGFULNESS
            
            Example items:
            - I am usually: (a) bored (b) neutral (c) excited about life
            - My life is: (a) empty and without purpose (b) routine (c) full of good things
            - I am: (a) undecided about my life goals (b) somewhat clear (c) very clear about my life goals
            
            Response format: 7-point bipolar scales
            """,
        },
        "MAPS": {
            "name": "Multidimensional Assessment of Purpose in Life (MAPS)",
            "structure": """
            The MAPS typically includes:
            
            Multiple dimensions:
            1. PURPOSE AWARENESS
            2. PURPOSE ENGAGEMENT
            3. PURPOSE ALIGNMENT
            4. PURPOSE MEANINGFULNESS
            
            Example items:
            - I have a clear sense of my purpose in life
            - I actively work toward my life purpose
            - My daily activities align with my life purpose
            - My purpose gives my life meaning and direction
            
            Response scale: 1 (Strongly disagree) to 7 (Strongly agree)
            """
        }
    }
    return examples

def read_thinker_text(thinker_name):
    """
    Read the thinker's meaning text from the thinkers_texts directory.
    
    Args:
        thinker_name (str): Name of the thinker
    
    Returns:
        str: Content of the thinker's text file
    """
    thinkers_dir = Path("../thinkers_texts")
    filename = f"{thinker_name.replace(' ', '_').lower()}_meaning.txt"
    filepath = thinkers_dir / filename
    
    if not filepath.exists():
        raise FileNotFoundError(f"Thinker text file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def generate_thinker_questionnaire(thinker_name, thinker_text, api_key=None, model="gpt-4"):
    """
    Generate a questionnaire based on a thinker's ideas about meaning.
    
    Args:
        thinker_name (str): Name of the thinker
        thinker_text (str): The thinker's text about meaning
        api_key (str): OpenAI API key (optional)
        model (str): OpenAI model to use
    
    Returns:
        str: Generated questionnaire text
    """
    client = setup_openai_client(api_key)
    
    # Get standard questionnaire examples
    examples = get_standard_questionnaire_examples()
    
    prompt = f"""
    Based on the following thinker's ideas about meaning, create a comprehensive questionnaire that captures their unique perspective on meaning in life.

    THINKER: {thinker_name}
    
    THINKER'S IDEAS ABOUT MEANING:
    {thinker_text}
    
    STANDARD QUESTIONNAIRE STRUCTURES TO USE AS TEMPLATES:
    {json.dumps(examples, indent=2)}
    
    TASK: Create a questionnaire that:
    1. Reflects {thinker_name}'s specific views on meaning and purpose
    2. Uses the structural elements from the standard questionnaires (scales, response formats, etc.)
    3. Includes 15-20 items that capture different aspects of their philosophy
    4. Has clear instructions and response scales
    5. Is suitable for research purposes
    
    REQUIREMENTS:
    - Include a title and brief description
    - Provide clear instructions for respondents
    - Use appropriate response scales (e.g., 1-7 Likert scales)
    - Group items into logical dimensions if applicable
    - Make items clear and accessible
    - Ensure items directly relate to {thinker_name}'s philosophical views
    
    FORMAT: Return the questionnaire in a clear, structured format with:
    - Title
    - Description
    - Instructions
    - Items grouped by dimensions (if applicable)
    - Response scale explanation
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert in psychological measurement and philosophy, specializing in creating valid questionnaires that capture philosophical concepts about meaning and purpose."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error generating questionnaire: {e}")
        return None

def save_questionnaire(thinker_name, questionnaire_text):
    """
    Save the generated questionnaire to a file in the generated_questionnaires directory.
    
    Args:
        thinker_name (str): Name of the thinker
        questionnaire_text (str): The generated questionnaire text
    """
    # Create generated_questionnaires directory if it doesn't exist
    questionnaires_dir = Path("../generated_questionnaires")
    questionnaires_dir.mkdir(exist_ok=True)
    
    # Create filename
    filename = f"{thinker_name.replace(' ', '_').lower()}_questionnaire.txt"
    filepath = questionnaires_dir / filename
    
    # Add metadata header
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"Generated on: {timestamp}\nThinker: {thinker_name}\nQuestionnaire Type: Meaning in Life\n{'='*50}\n\n"
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(questionnaire_text)
    
    print(f"Questionnaire saved to: {filepath}")
    return filepath

def main():
    parser = argparse.ArgumentParser(description='Generate questionnaires based on thinkers\' ideas about meaning')
    parser.add_argument('thinker_name', help='Name of the thinker/philosopher')
    parser.add_argument('--api-key', help='OpenAI API key (optional if set as environment variable)')
    parser.add_argument('--model', default='gpt-4', help='OpenAI model to use (default: gpt-4)')
    
    args = parser.parse_args()
    
    print(f"Generating questionnaire based on {args.thinker_name}'s ideas about meaning...")
    
    try:
        # Read the thinker's text
        thinker_text = read_thinker_text(args.thinker_name)
        print(f"✅ Loaded {args.thinker_name}'s text ({len(thinker_text)} characters)")
        
        # Generate the questionnaire
        questionnaire = generate_thinker_questionnaire(args.thinker_name, thinker_text, args.api_key, args.model)
        
        if questionnaire:
            # Save to file
            filepath = save_questionnaire(args.thinker_name, questionnaire)
            print(f"\n✅ Questionnaire generated successfully!")
            print(f"📁 File saved: {filepath}")
        else:
            print("❌ Failed to generate questionnaire.")
            
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure the thinker's text file exists in ../thinkers_texts/")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
