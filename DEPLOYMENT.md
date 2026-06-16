# Jamarik Technologies Django - Render Deployment Guide

## Overview
This Django project is configured for production deployment on Render.com. This guide covers all necessary steps to ensure a successful deployment.

---

## Prerequisites Checklist
- [ ] GitHub account with the project repository
- [ ] Render.com account (free tier available)
- [ ] PostgreSQL knowledge (basic understanding)
- [ ] Environment variables ready (see `.env.example`)

---

## Part 1: Pre-Deployment Setup (Local)

### 1.1 Environment Variables
Copy `.env.example` to `.env` and fill in all values:

```bash
cp .env.example .env
```

**Required variables:**
- `SECRET_KEY`: Generate using `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- `EMAIL_HOST_USER`: Gmail account for sending emails
- `EMAIL_HOST_PASSWORD`: Gmail App Password (NOT regular password)
- `DEBUG=False` for production testing

### 1.2 Local Testing
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Test the server locally
python manage.py runserver
# Visit http://localhost:8000 to verify
```

### 1.3 Test Production Settings
```bash
# Set production environment variables
export DEBUG=False
export ENVIRONMENT=production
export SECRET_KEY=your-generated-secret-key

# Verify Django system checks
python manage.py check
```

---

## Part 2: GitHub Setup

### 2.1 Ensure .env is NOT committed
Verify `.env` is in `.gitignore`:
```bash
grep "\.env" .gitignore
# Should return: .env
```

### 2.2 Push to GitHub
```bash
git add .
git commit -m "feat: Prepare for Render deployment - add render.yaml, security hardening"
git push origin main
```

---

## Part 3: Render Deployment

### 3.1 Connect GitHub to Render

1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Select "Connect Repository"
4. Authorize GitHub and select this repository
5. Configure settings:
   - **Name**: `jamarik-website` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: (Should auto-detect from render.yaml)
   - **Start Command**: (Should auto-detect from render.yaml)

### 3.2 Set Environment Variables in Render Dashboard

Go to your service settings → "Environment" tab and add:

**CRITICAL - Must be set:**
```
SECRET_KEY=<generate-new-secret-key>
ENVIRONMENT=production
```

**Email Configuration (if using Gmail):**
```
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@jamarik.com
CONTACT_EMAIL=info@jamarik.com
```

**Other Settings:**
```
DEBUG=False
```

### 3.3 Create PostgreSQL Database

1. In Render Dashboard, click "New +" → "PostgreSQL"
2. Name it: `jamarik-db`
3. Region: Same as your web service
4. Plan: Free tier for testing, Starter for production
5. Select "Create Database"
6. Copy the connection string (it will auto-populate as DATABASE_URL)

### 3.4 Deploy

Click "Deploy" in your service settings. Monitor the deployment:
- Build logs will show Django setup, migrations, and static file collection
- Watch for any errors in the logs

---

## Part 4: Post-Deployment Verification

### 4.1 Check Deployment Status
1. Visit your deployed app: `https://jamarik-website.onrender.com`
2. Verify homepage loads correctly
3. Check navigation links work
4. Test contact form submission

### 4.2 Admin Access
1. Create superuser via Render console:
   ```bash
   render run python manage.py createsuperuser
   ```
2. Visit `https://jamarik-website.onrender.com/admin/`
3. Log in with superuser credentials

### 4.3 Check Security Headers
Use an online tool or browser dev tools:
- Verify HTTPS is enforced
- Check security headers are present:
  - `Strict-Transport-Security`
  - `X-Content-Type-Options`
  - `X-Frame-Options`
  - `X-XSS-Protection`

### 4.4 Email Testing
1. Go to Admin → Core → Contact Messages
2. Send a test contact form
3. Verify email is received (check spam folder)

---

## Part 5: Troubleshooting

### Deployment Failed - Build Error
**Check logs in Render Dashboard:**
1. Click on your service
2. Go to "Logs" tab
3. Look for error messages
4. Common issues:
   - Missing SECRET_KEY → Set in Environment tab
   - Database connection error → Verify DATABASE_URL
   - Pillow installation error → Check requirements.txt has pillow

### Static Files Not Loading
```bash
# Render should auto-run collectstatic, but if not:
render run python manage.py collectstatic --noinput
```

### Database Migration Error
```bash
# Check migration status
render run python manage.py showmigrations

# Apply pending migrations
render run python manage.py migrate
```

### Email Not Sending
1. Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in Environment
2. Gmail: Ensure 2FA enabled and use App Password (not account password)
3. Check firewall: port 587 must be open
4. Test locally first to confirm settings

### "SECRET_KEY required for production" Error
1. Go to Render Dashboard → Environment tab
2. Add `SECRET_KEY` variable
3. Redeploy your service

---

## Part 6: Ongoing Maintenance

### Regular Tasks
- Monitor logs weekly for errors
- Check Admin → Contact Messages for customer inquiries
- Update blog/portfolio through Admin panel
- Backup database regularly (Render offers automated backups on paid plans)

### Updates
When updating code:
```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```
Render automatically redeploys when you push to main.

### Database Backups
1. Render free tier: Limited retention
2. For production: Consider upgrade to Starter+ for better backups
3. Manual backup: Export database through Render dashboard

---

## Part 7: Production Checklist

### Before Going Live
- [ ] SECRET_KEY is unique and strong
- [ ] DEBUG=False in environment
- [ ] ALLOWED_HOSTS configured correctly
- [ ] Email configuration working
- [ ] Database migrations completed
- [ ] Static files loading correctly
- [ ] Admin interface accessible
- [ ] Contact form tested
- [ ] HTTPS enforced
- [ ] No sensitive data in logs
- [ ] Domain name configured (if custom domain)

### Custom Domain Setup (Optional)
1. In Render Dashboard → Custom Domain
2. Add your domain name
3. Update DNS records with Render-provided values
4. Wait for SSL certificate (usually 5-10 minutes)

---

## Support & Documentation

- Render Documentation: https://render.com/docs
- Django Documentation: https://docs.djangoproject.com
- GitHub Issues: Report deployment issues here
- Contact: info@jamarik.com

---

## Security Notes

⚠️ **IMPORTANT:**
1. Never commit `.env` file to GitHub
2. Never share SECRET_KEY publicly
3. Never use hardcoded credentials in code
4. Rotate SECRET_KEY periodically
5. Use strong, unique database passwords
6. Monitor logs for suspicious activity
7. Keep Django and dependencies updated

---

## Scaling Beyond Free Tier

When ready to scale:
1. Upgrade database to Starter ($7/month)
2. Consider upgrading web service for better performance
3. Add monitoring and alerting
4. Consider CDN for static files
5. Implement caching strategy

---

Generated: 2026-06-16
Project: Jamarik Technologies Ltd
