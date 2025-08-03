import subprocess
import sys
import time
from pathlib import Path

def run_questionnaire_generation(thinker_name, api_key=None):
    """
    Run the questionnaire generation script for a specific thinker.
    
    Args:
        thinker_name (str): Name of the thinker
        api_key (str): OpenAI API key (optional)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Build the command
        cmd = [sys.executable, "generate_thinker_questionnaires.py", thinker_name]
        
        if api_key:
            cmd.extend(["--api-key", api_key])
        
        print(f"\n{'='*60}")
        print(f"Generating questionnaire for: {thinker_name}")
        print(f"{'='*60}")
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✅ Successfully generated questionnaire for {thinker_name}")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Failed to generate questionnaire for {thinker_name}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {thinker_name}: {e}")
        return False

def get_available_thinkers():
    """
    Get list of available thinkers from the thinkers_texts directory.
    """
    thinkers_dir = Path("../thinkers_texts")
    thinkers = []
    
    if thinkers_dir.exists():
        for file in thinkers_dir.glob("*_meaning.txt"):
            # Extract thinker name from filename
            thinker_name = file.stem.replace("_meaning", "").replace("_", " ").title()
            # Handle special cases
            if thinker_name == "Jean-paul Sartre":
                thinker_name = "Jean-Paul Sartre"
            elif thinker_name == "Søren Kierkegaard":
                thinker_name = "Søren Kierkegaard"
            thinkers.append(thinker_name)
    
    return sorted(thinkers)

def main():
    # Get available thinkers
    thinkers = get_available_thinkers()
    
    if not thinkers:
        print("❌ No thinker text files found in ../thinkers_texts/")
        print("Please run the batch_generate_thinkers.py script first to create thinker essays.")
        return
    
    # Get API key from environment or user input
    api_key = None
    if not api_key:
        api_key = input("Enter your OpenAI API key (or press Enter if set as environment variable): ").strip()
        if not api_key:
            api_key = None
    
    print(f"\n🚀 Starting batch questionnaire generation for {len(thinkers)} thinkers...")
    print(f"Thinkers to process: {', '.join(thinkers)}")
    
    successful = 0
    failed = 0
    
    for i, thinker in enumerate(thinkers, 1):
        print(f"\n📝 Processing {i}/{len(thinkers)}: {thinker}")
        
        if run_questionnaire_generation(thinker, api_key):
            successful += 1
        else:
            failed += 1
        
        # Add a small delay between requests to be respectful to the API
        if i < len(thinkers):  # Don't wait after the last one
            print("⏳ Waiting 3 seconds before next request...")
            time.sleep(3)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"🎉 BATCH QUESTIONNAIRE GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total processed: {len(thinkers)}")
    
    if successful > 0:
        print(f"\n📁 Generated questionnaires saved in: ../generated_questionnaires/")
        print("Files created:")
        questionnaires_dir = Path("../generated_questionnaires")
        if questionnaires_dir.exists():
            for file in questionnaires_dir.glob("*_questionnaire.txt"):
                print(f"  - {file.name}")

if __name__ == "__main__":
    main()
