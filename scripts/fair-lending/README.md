# Fair-lending starter kit

Standalone Flask prototype from the fair-lending hackathon direction. Includes:

- **Eng A:** LLM-powered lending decision engine (target)
- **Eng B:** RedLayer paired-testing engine (matched pairs, disparity detection, Risk Score)

## Quick start

```bash
cd scripts/fair-lending
pip install flask openai
export OPENAI_API_KEY="sk-your-key-here"
python starter_kit.py
# Open http://localhost:5000
```

For a public demo link, tunnel port 5000 (e.g. with ngrok).

See [docs/fair-lending/](../../docs/fair-lending/) for the full plan and legal language guide.
