# 🤝 Contributing to MedReel Analyzer

First off, thanks for taking the time to contribute! 🎉

## 🌟 How Can I Contribute?

### 🐛 Reporting Bugs

Found a bug? Here's how to report it:

1. **Check existing issues** to avoid duplicates
2. **Open a new issue** with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if possible
   - Your environment (OS, Python version)

### 💡 Suggesting Features

Have an idea? We'd love to hear it!

1. **Check existing feature requests**
2. **Open a new issue** with:
   - Clear description of the feature
   - Why it would be useful
   - How it might work
   - Any relevant examples

### 🔧 Pull Requests

Ready to code? Follow these steps:

1. **Fork the repository**
2. **Create a branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Amazing new feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/AmazingFeature
   ```
7. **Open a Pull Request**

## 📝 Code Style Guidelines

### Python Code

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

Example:
```python
def transcribe_audio(audio_path: str, language: str) -> str:
    """
    Transcribe audio file to text.
    
    Args:
        audio_path: Path to audio file
        language: Language code ('Hindi' or 'English')
    
    Returns:
        Transcribed text as string
    """
    # Implementation
    pass
```

### Commit Messages

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Maintenance tasks

Examples:
```bash
git commit -m "feat: Add support for Spanish transcription"
git commit -m "fix: Resolve FFmpeg path issue on Windows"
git commit -m "docs: Update installation instructions"
```

## 🧪 Testing

Before submitting:

1. **Test locally**
   ```bash
   streamlit run app.py
   ```

2. **Test with different inputs**
   - Hindi Reels
   - English Reels
   - Long Reels
   - Short Reels

3. **Check for errors**
   - Watch console logs
   - Try edge cases
   - Test on different browsers

## 📚 Areas for Contribution

### High Priority

- [ ] Add more languages (Spanish, French, etc.)
- [ ] Improve transcription accuracy
- [ ] Add more medical databases
- [ ] Performance optimization
- [ ] Better error handling

### Medium Priority

- [ ] Add video download option
- [ ] Export to PDF
- [ ] Batch processing
- [ ] Mobile UI improvements
- [ ] Add tests

### Nice to Have

- [ ] Voice input for questions
- [ ] Share analysis feature
- [ ] Browser extension
- [ ] API endpoint
- [ ] Admin dashboard

## 🎯 Focus Areas

### 1. Accuracy Improvements

Help improve medical fact-checking:
- Better PubMed queries
- Additional medical APIs
- Improved prompt engineering
- Citation system

### 2. User Experience

Make it more Gen-Z friendly:
- UI/UX improvements
- Animation effects
- Better error messages
- Loading states

### 3. Performance

Speed things up:
- Optimize transcription
- Faster API calls
- Better caching
- Async processing

### 4. Accessibility

Make it accessible:
- Screen reader support
- Keyboard navigation
- High contrast mode
- Better mobile support

## 🚀 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/medreel-analyzer.git
cd medreel-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API keys

# Run the app
streamlit run app.py
```

## 📖 Documentation

When adding features:

1. **Update README.md** if needed
2. **Add docstrings** to new functions
3. **Update DEPLOYMENT.md** if deployment changes
4. **Add examples** in comments

## ❓ Questions?

- **GitHub Discussions:** Ask questions
- **Issues:** Report bugs
- **Email:** [your-email@example.com]

## 🎉 Recognition

Contributors will be:
- Listed in README.md
- Credited in release notes
- Mentioned in announcements

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

✅ **Do:**
- Be respectful and inclusive
- Give constructive feedback
- Accept criticism gracefully
- Focus on what's best for the community

❌ **Don't:**
- Use inappropriate language
- Troll or insult others
- Publish others' private information
- Engage in any unprofessional conduct

### Enforcement

Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report issues to: [email@example.com]

## 🙏 Thank You!

Every contribution, no matter how small, is appreciated!

Happy coding! 💜✨
