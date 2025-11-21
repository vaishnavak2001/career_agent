# Security Policy

## 🔒 Protecting Your Sensitive Information

This application handles sensitive data including API keys, email credentials, and personal information. Please follow these security guidelines.

## ⚠️ NEVER Commit These Files

The following files contain sensitive information and should **NEVER** be committed to version control:

- `.env` - Contains API keys and passwords
- `*.db` files - Contains your personal job search data
- Any files with real credentials

These are already excluded in `.gitignore`, but always verify before committing.

## ✅ Secure Configuration

### 1. Environment Variables Setup

**Always use the `.env.example` as a template:**

```bash
# Copy the example file
cp .env.example .env

# Edit with your REAL credentials (this file is gitignored)
nano .env
```

### 2. API Keys

**OpenAI API Key:**
- Never share your API key
- Rotate keys periodically
- Use environment variables only
- Monitor usage at https://platform.openai.com/usage

**Email Credentials:**
- Use App Passwords, not regular passwords
- For Gmail: https://myaccount.google.com/apppasswords
- Limit permissions to SMTP only if possible

### 3. Database Security

**SQLite (Default):**
- `career_agent.db` contains your personal data
- Excluded from git by default
- Backup regularly to a secure location
- Don't share database files

**PostgreSQL:**
- Use strong passwords
- Don't expose database ports publicly
- Use SSL/TLS connections
- Regular backups

## 🛡️ Best Practices

### For Users

1. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Review Permissions**
   - Understand what data the scraper collects
   - Review email notification templates
   - Check auto-apply settings

3. **Secure Your Machine**
   - Use full disk encryption
   - Lock your computer when away
   - Use strong passwords

4. **Dry Run Mode**
   - Keep `DRY_RUN=true` in production
   - Test thoroughly before auto-applying
   - Review generated cover letters

### For Developers

1. **Code Review**
   - Never hardcode secrets
   - Use `os.getenv()` for all sensitive data
   - Validate all user inputs
   - Sanitize data before database insertion

2. **Testing**
   - Use mock credentials for tests
   - Don't commit test databases
   - Clean up test data

3. **Pull Requests**
   - Check for exposed secrets
   - Review `.gitignore` changes
   - Validate environment variable usage

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email the maintainer privately
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if known)

## 📋 Security Checklist

Before deploying or sharing:

- [ ] `.env` file is NOT in version control
- [ ] `.env.example` has placeholder values only
- [ ] Database files are excluded
- [ ] API keys are in environment variables
- [ ] `DRY_RUN=true` is set
- [ ] `.gitignore` is configured correctly
- [ ] No hardcoded credentials in code
- [ ] Dependencies are up to date
- [ ] SMTP credentials use App Passwords

## 🔧 Environment Variables Reference

**Required for Full Functionality:**
- `OPENAI_API_KEY` - For AI features (cover letters, matching)

**Optional but Recommended:**
- `DATABASE_URL` - For PostgreSQL (default: SQLite)
- `SENDER_EMAIL` - For email notifications
- `SENDER_PASSWORD` - App password for email
- `RECIPIENT_EMAIL` - Where to send notifications

**Safety Settings:**
- `DRY_RUN` - Prevent actual application submissions (default: true)
- `MIN_MATCH_SCORE` - Minimum score to apply (default: 70)

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

**Remember: Security is a shared responsibility. Stay vigilant! 🛡️**
