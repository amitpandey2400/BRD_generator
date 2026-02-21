# 🎉 Google Gemini API Setup Guide (FREE!)

## Why Gemini?
✅ **Generous Free Tier**: 15 requests/minute, 1M tokens/minute, 1,500 requests/day  
✅ **Fast & Accurate**: Gemini 1.5 Flash is optimized for speed  
✅ **No Credit Card Required**: Completely free to start  

## Step 1: Get Your Free Gemini API Key

1. **Go to Google AI Studio**  
   Visit: https://ai.google.dev/

2. **Sign in with Google Account**  
   Use any Google account (Gmail)

3. **Get API Key**  
   - Click on "Get API Key" in the top right
   - Click "Create API Key"
   - Select "Create API key in new project" or use existing one
   - Copy your API key (starts with `AIza...`)

## Step 2: Update Your .env File

Open your `.env` file and add your Gemini API key:

```env
# Google Gemini Configuration (FREE TIER AVAILABLE!)
GEMINI_API_KEY=AIzaSy...your-actual-key-here...
GEMINI_MODEL=gemini-1.5-flash
AI_PROVIDER=gemini
```

**Available Models:**
- `gemini-1.5-flash` - Fast, efficient (recommended for most uses)
- `gemini-1.5-pro` - More capable, slightly slower

## Step 3: Restart Your Application

```powershell
# Stop the current server (Ctrl+C if running)

# Restart with new configuration
& ".venv\Scripts\Activate.ps1"
python main.py
```

## Step 4: Test It!

Your application will now use Gemini API instead of OpenAI!

Test by visiting:
- http://localhost:8000/docs
- Create a project and upload a document

## Switching Between Providers

You can easily switch between OpenAI and Gemini:

**To use Gemini (Free):**
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your-key-here
```

**To use OpenAI (Paid):**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

## Free Tier Limits

**Gemini Free Tier:**
- 15 requests per minute
- 1 million tokens per minute
- 1,500 requests per day

This is more than enough for development and testing!

## Troubleshooting

**Error: "GEMINI_API_KEY not set"**
- Make sure you added the key to `.env` file
- Restart the application after updating `.env`

**Error: "API key not valid"**
- Check that you copied the full API key from Google AI Studio
- Make sure there are no extra spaces in the `.env` file

**Rate limit exceeded:**
- Free tier has limits (see above)
- Wait a minute and try again
- Consider spacing out your requests

## Need Help?

- **Google AI Documentation**: https://ai.google.dev/docs
- **Get API Key**: https://ai.google.dev/
- **Free Tier Details**: https://ai.google.dev/pricing

---

**🎉 You're all set! Your BRD Generator now runs on FREE Gemini AI!**
