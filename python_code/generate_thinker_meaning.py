import os
import openai
from pathlib import Path
import argparse
from datetime import datetime

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

def generate_thinker_meaning_essay(thinker_name, api_key=None, model="gpt-4"):
    """
    Generate a 1-page essay about a thinker's ideas on meaning.
    
    Args:
        thinker_name (str): Name of the thinker/philosopher
        api_key (str): OpenAI API key (optional, can use environment variable)
        model (str): OpenAI model to use
    
    Returns:
        str: Generated essay text
    """
    client = setup_openai_client(api_key)
    
    prompt = f"""
    Write a comprehensive 1-page essay (approximately 500-600 words) about {thinker_name}'s ideas and philosophy regarding the meaning of life and human existence.
    
    The essay should include:
    1. A brief introduction to the thinker and their general philosophical approach
    2. Their specific views on meaning in life
    3. Key concepts and arguments they developed about meaning
    4. How their ideas relate to or differ from other philosophical perspectives
    5. The relevance and implications of their views on meaning for contemporary understanding
    
    Write in an academic but accessible style, suitable for research purposes. 
    Focus on their most important contributions to the philosophy of meaning.
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a knowledgeable philosophy researcher specializing in the study of meaning and purpose in human existence."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error generating essay: {e}")
        return None

def save_thinker_essay(thinker_name, essay_text):
    """
    Save the generated essay to a file in the thinkers_texts directory.
    
    Args:
        thinker_name (str): Name of the thinker
        essay_text (str): The generated essay text
    """
    # Create thinkers_texts directory if it doesn't exist
    thinkers_dir = Path("../thinkers_texts")
    thinkers_dir.mkdir(exist_ok=True)
    
    # Create filename
    filename = f"{thinker_name.replace(' ', '_').lower()}_meaning.txt"
    filepath = thinkers_dir / filename
    
    # Add metadata header
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"Generated on: {timestamp}\nThinker: {thinker_name}\n{'='*50}\n\n"
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(essay_text)
    
    print(f"Essay saved to: {filepath}")
    return filepath

def main():
    parser = argparse.ArgumentParser(description='Generate thinker meaning essays using GPT')
    parser.add_argument('thinker_name', help='Name of the thinker/philosopher')
    parser.add_argument('--api-key', help='OpenAI API key (optional if set as environment variable)')
    parser.add_argument('--model', default='gpt-4', help='OpenAI model to use (default: gpt-4)')
    
    args = parser.parse_args()
    
    print(f"Generating essay about {args.thinker_name}'s ideas on meaning...")
    
    # Generate the essay
    essay = generate_thinker_meaning_essay(args.thinker_name, args.api_key, args.model)
    
    if essay:
        # Save to file
        filepath = save_thinker_essay(args.thinker_name, essay)
        print(f"\nEssay generated successfully!")
        print(f"File saved: {filepath}")
    else:
        print("Failed to generate essay.")

if __name__ == "__main__":
    main()
