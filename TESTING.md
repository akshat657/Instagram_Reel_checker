# 🧪 Testing Guide for MedReel Analyzer

Complete guide to test your app before deployment.

## 🎯 Pre-Deployment Testing Checklist

### ✅ Local Testing

Run through this checklist before deploying:

#### 1. Installation Test

```bash
# Test virtual environment creation
python -m venv test_venv
source test_venv/bin/activate  # or test_venv\Scripts\activate on Windows

# Test dependency installation
pip install -r requirements.txt

# Verify FFmpeg
ffmpeg -version
```

**Expected:** All dependencies install without errors, FFmpeg is available.

#### 2. Environment Variables Test

```bash
# Create .env file
cp .env.example .env

# Add test API keys
# Open .env and add your 3 Groq API keys
```

**Expected:** .env file created with valid API keys.

#### 3. App Launch Test

```bash
streamlit run app.py
```

**Expected:** 
- App opens at `http://localhost:8501`
- No error messages in console
- UI loads correctly
- Title displays: "💊 MedReel Analyzer 🎥"

### ✅ Functionality Testing

#### Test Case 1: Basic Reel Analysis (Hindi)

**Steps:**
1. Paste Hindi Reel URL
2. Select "Hindi" language
3. Click "Analyze This Reel!"

**Test URL:**
```
https://www.instagram.com/reel/DUV5eiCieMQ/?igsh=MThheHFwOWpwMjk5Zw%3D%3D
```

**Expected Results:**
- ✅ Caption displays correctly
- ✅ Transcript in Hindi (Devanagari script)
- ✅ AI analysis appears
- ✅ Download buttons work
- ✅ Chat section appears

#### Test Case 2: Basic Reel Analysis (English)

**Steps:**
1. Paste English Reel URL
2. Select "English" language
3. Click "Analyze This Reel!"

**Expected Results:**
- ✅ Caption displays correctly
- ✅ Transcript in English
- ✅ AI analysis appears
- ✅ Medical references included

#### Test Case 3: Chat Functionality

**Steps:**
1. After analyzing a reel
2. Type question: "Is this claim accurate?"
3. Click Send

**Expected Results:**
- ✅ Question appears in chat
- ✅ AI response appears
- ✅ Response is relevant to reel content
- ✅ Chat history persists

#### Test Case 4: Download Features

**Steps:**
1. After analyzing a reel
2. Click each download button

**Expected Results:**
- ✅ caption.txt downloads
- ✅ transcript.txt downloads
- ✅ analysis.txt downloads
- ✅ Files contain correct data

#### Test Case 5: API Fallback

**Steps:**
1. Use invalid API key in GROQ_API_KEY_1
2. Analyze a reel

**Expected Results:**
- ✅ Warning message: "API Key 1 failed, trying next..."
- ✅ App switches to API Key 2
- ✅ Analysis completes successfully

### ✅ UI/UX Testing

#### Test Case 6: Dark Mode

**Steps:**
1. Change browser/system to dark mode
2. Check app appearance

**Expected Results:**
- ✅ Background is dark
- ✅ Text is visible (light colored)
- ✅ Buttons are visible
- ✅ Chat messages readable

#### Test Case 7: Light Mode

**Steps:**
1. Change browser/system to light mode
2. Check app appearance

**Expected Results:**
- ✅ Background is light
- ✅ Text is visible (dark colored)
- ✅ Proper contrast
- ✅ Professional look

#### Test Case 8: Mobile Responsive

**Steps:**
1. Open app on mobile browser OR resize browser to mobile size
2. Test all features

**Expected Results:**
- ✅ Layout adapts to mobile
- ✅ Buttons are tappable
- ✅ Text is readable
- ✅ No horizontal scrolling

### ✅ Error Handling Testing

#### Test Case 9: Invalid URL

**Steps:**
1. Enter: "not-a-url"
2. Click analyze

**Expected Results:**
- ✅ Error message displays
- ✅ App doesn't crash
- ✅ User can try again

#### Test Case 10: Network Error

**Steps:**
1. Disconnect internet
2. Try to analyze reel

**Expected Results:**
- ✅ Graceful error message
- ✅ No crash
- ✅ Helpful error text

#### Test Case 11: Long Reel

**Steps:**
1. Use a 2+ minute reel
2. Analyze

**Expected Results:**
- ✅ Progress indicator shows
- ✅ Transcription completes (may take time)
- ✅ No timeout errors

### ✅ Performance Testing

#### Test Case 12: Speed Test

**Measure:**
- Time to fetch reel data: < 5 seconds
- Time to transcribe 30s reel: < 30 seconds
- Time to get AI analysis: < 10 seconds

**How to Test:**
```bash
# Check logs in terminal for timing
# Look for processing messages
```

#### Test Case 13: Memory Usage

**Steps:**
1. Analyze 5 reels in succession
2. Monitor memory

**Expected:**
- ✅ Memory doesn't keep increasing
- ✅ Temp files are cleaned
- ✅ No memory leaks

### ✅ Security Testing

#### Test Case 14: API Key Protection

**Steps:**
1. Check network tab in browser
2. Analyze a reel

**Expected:**
- ✅ API keys not visible in network requests
- ✅ API keys not in page source
- ✅ Keys only in backend

#### Test Case 15: Input Sanitization

**Steps:**
1. Try malicious inputs:
   - `<script>alert('test')</script>`
   - `'; DROP TABLE users; --`

**Expected:**
- ✅ Input is sanitized
- ✅ No code execution
- ✅ Safe error handling

## 🚀 Pre-Deployment Checklist

Before deploying to Streamlit Cloud:

- [ ] All local tests pass
- [ ] `.gitignore` includes `.env`
- [ ] `packages.txt` includes `ffmpeg`
- [ ] `requirements.txt` is complete
- [ ] README.md is updated
- [ ] All API keys are valid
- [ ] No hardcoded secrets in code

## 📊 Testing Results Template

Use this template to record results:

```markdown
## Test Results - [Date]

### Environment
- OS: 
- Python Version: 
- Browser: 

### Test Results

| Test Case | Status | Notes |
|-----------|--------|-------|
| Installation | ✅/❌ | |
| Hindi Analysis | ✅/❌ | |
| English Analysis | ✅/❌ | |
| Chat Function | ✅/❌ | |
| Downloads | ✅/❌ | |
| API Fallback | ✅/❌ | |
| Dark Mode | ✅/❌ | |
| Light Mode | ✅/❌ | |
| Mobile View | ✅/❌ | |
| Error Handling | ✅/❌ | |

### Issues Found
1. 
2. 

### Recommendations
1. 
2. 
```

## 🐛 Common Issues & Solutions

### Issue: FFmpeg not found
**Solution:** Install FFmpeg for your OS

### Issue: Transcription empty
**Solution:** Check audio quality, try different language setting

### Issue: API rate limit
**Solution:** Wait 60 seconds or use different API key

### Issue: Slow performance
**Solution:** Use shorter reels for testing

## 📞 Reporting Test Results

After testing:
1. Create an issue with test results
2. Use the template above
3. Include screenshots if relevant
4. Tag with `testing` label

## 🎉 Success Criteria

Your app is ready to deploy if:
- ✅ All critical test cases pass
- ✅ No crashes or errors
- ✅ UI looks good in both themes
- ✅ Chat works correctly
- ✅ Downloads work
- ✅ API fallback functions

Happy Testing! 🧪✨
