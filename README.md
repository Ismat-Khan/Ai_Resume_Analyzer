# 💗 PinkCV — AI Resume Analyzer

A clean, modular Streamlit app that compares a PDF resume with a pasted job description using the Groq API and strict structured JSON output.

## Features

- PDF resume upload
- Job description input
- PDF text extraction with pypdf
- Groq AI analysis
- Strict JSON Schema structured output
- Pydantic validation
- Overall match score
- Matching skills
- Missing skills
- ATS keywords found/missing
- Resume-specific problems
- Actionable recommendations
- Final result
- Light pink glassmorphism UI
- Streamlit Cloud ready

## Project structure

```text
ai-resume-analyzer/
├── app.py
├── config.py
├── resume_parser.py
├── schemas.py
├── groq_analyzer.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

## Local setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install packages

```bash
pip install -r requirements.txt
```

### 3. Configure the Groq key

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY = "your-real-groq-api-key"
```

Never commit that file.

### 4. Run

```bash
streamlit run app.py
```

## Streamlit Cloud

1. Push these files to GitHub.
2. Create a Streamlit Community Cloud app.
3. Select the repository and branch.
4. Set the main file to `app.py`.
5. In the app's Secrets settings, add:

```toml
GROQ_API_KEY = "your-real-groq-api-key"
```

6. Deploy.

## Notes

- The app uses Groq's OpenAI-compatible Chat Completions API.
- The default model is `openai/gpt-oss-120b`, which is used with Groq structured outputs.
- The PDF should contain selectable text. Scanned/image-only PDFs may need OCR, which this version intentionally does not add.
- The match score is an AI-generated analytical estimate, not a guarantee of ATS screening or hiring.
- Recommendations should only be applied when they truthfully represent the candidate's real experience.
