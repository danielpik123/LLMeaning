# LLMeaning - Meaning Questionnaires Research

A comprehensive research toolkit for generating philosophical essays and psychological questionnaires based on thinkers' views on meaning in life.

## Overview

This project provides automated tools to:
1. Generate comprehensive essays about philosophers' views on meaning
2. Create research-ready questionnaires based on these philosophical perspectives
3. Process multiple thinkers in batch operations
4. Maintain organized research outputs with proper metadata

## Quick Start

1. **Install dependencies:**
```bash
cd python_code
pip install -r requirements.txt
```

2. **Set up your OpenAI API key:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

3. **Generate thinker essays:**
```bash
python batch_generate_thinkers.py
```

4. **Generate questionnaires:**
```bash
python batch_generate_questionnaires.py
```

## Project Structure

```
LLMeaning/
├── python_code/                    # All Python scripts
│   ├── generate_thinker_meaning.py      # Individual essay generation
│   ├── batch_generate_thinkers.py       # Batch essay generation
│   ├── generate_thinker_questionnaires.py # Individual questionnaire generation
│   ├── batch_generate_questionnaires.py  # Batch questionnaire generation
│   └── requirements.txt                  # Dependencies
├── thinkers_texts/                  # Generated thinker essays
├── generated_questionnaires/        # Generated questionnaires
├── standard_questionnaires/         # Reference questionnaire structures
└── research_notes/                  # Research documentation
```

## Features

- **Professional logging** with configurable verbosity
- **Robust error handling** for API failures
- **Rate limiting** with respectful API usage
- **Metadata management** with automatic timestamps
- **Cross-platform compatibility** with proper path handling

## Example Thinkers

Currently includes essays and questionnaires for:
- Viktor Frankl (Logotherapy, Tragic Optimism)
- Albert Camus (Absurdism, Existentialism)
- Jean-Paul Sartre (Existentialism, Freedom)
- Friedrich Nietzsche (Will to Power, Eternal Recurrence)
- Søren Kierkegaard (Faith, Despair, Subjective Truth)

## Usage Examples

### Generate a single thinker's essay:
```bash
python generate_thinker_meaning.py "Viktor Frankl"
```

### Generate a questionnaire based on a thinker:
```bash
python generate_thinker_questionnaires.py "Albert Camus"
```

### Batch process all thinkers:
```bash
python batch_generate_thinkers.py
python batch_generate_questionnaires.py
```

## Technical Details

- **API Integration**: OpenAI GPT-4/GPT-3.5-turbo support
- **File Management**: Automatic directory creation, UTF-8 encoding
- **Code Quality**: Comprehensive documentation, PEP 8 compliance
- **Security**: Proper API key management, .gitignore protection

## License

This project is designed for academic research purposes. Please ensure compliance with OpenAI's terms of service and relevant academic guidelines.

## Contributing

When contributing:
1. Maintain professional code standards
2. Add comprehensive documentation
3. Include proper error handling
4. Test with multiple thinkers
5. Update requirements.txt as needed
