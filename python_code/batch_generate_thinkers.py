import subprocess
import sys
import time
from pathlib import Path

def run_thinker_generation(thinker_name, api_key=None):
    """
    Run the thinker meaning generation script for a specific thinker.
    
    Args:
        thinker_name (str): Name of the thinker
        api_key (str): OpenAI API key (optional)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Build the command
        cmd = [sys.executable, "generate_thinker_meaning.py", thinker_name]
        
        if api_key:
            cmd.extend(["--api-key", api_key])
        
        print(f"\n{'='*60}")
        print(f"Generating essay for: {thinker_name}")
        print(f"{'='*60}")
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✅ Successfully generated essay for {thinker_name}")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Failed to generate essay for {thinker_name}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {thinker_name}: {e}")
        return False

def main():
    # List of thinkers to process (first 5 from README)
    thinkers = [
        "Viktor Frankl",
        "Albert Camus", 
        "Jean-Paul Sartre",
        "Friedrich Nietzsche",
        "Søren Kierkegaard"
    ]
    
    # Get API key from environment or user input
    api_key = None
    if not api_key:
        api_key = input("Enter your OpenAI API key (or press Enter if set as environment variable): ").strip()
        if not api_key:
            api_key = None
    
    print(f"\n🚀 Starting batch generation for {len(thinkers)} thinkers...")
    print(f"Thinkers to process: {', '.join(thinkers)}")
    
    successful = 0
    failed = 0
    
    for i, thinker in enumerate(thinkers, 1):
        print(f"\n📝 Processing {i}/{len(thinkers)}: {thinker}")
        
        if run_thinker_generation(thinker, api_key):
            successful += 1
        else:
            failed += 1
        
        # Add a small delay between requests to be respectful to the API
        if i < len(thinkers):  # Don't wait after the last one
            print("⏳ Waiting 2 seconds before next request...")
            time.sleep(2)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"🎉 BATCH PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total processed: {len(thinkers)}")
    
    if successful > 0:
        print(f"\n📁 Generated essays saved in: ../thinkers_texts/")
        print("Files created:")
        thinkers_dir = Path("../thinkers_texts")
        if thinkers_dir.exists():
            for file in thinkers_dir.glob("*_meaning.txt"):
                print(f"  - {file.name}")

if __name__ == "__main__":
    main()
