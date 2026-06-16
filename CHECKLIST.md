# PRODUCTION DEPLOYMENT CHECKLIST
# Jamarik Technologies Django Project

## 🔒 SECURITY REQUIREMENTS (CRITICAL)

### Environment Variables
- [ ] SECRET_KEY is set and unique
- [ ] SECRET_KEY is NOT in code or git history
- [ ] DEBUG=False in production environment
- [ ] ENVIRONMENT=production variable set
- [ ] All email credentials configured
- [ ] DATABASE_URL properly configured (auto on Render)
- [ ] No .env file is committed to GitHub

### Code Security
- [ ] No hardcoded passwords in source code
- [ ] No API keys in configuration
- [ ] No database credentials in code
- [ ] No email passwords in code
- [ ] .gitignore properly excludes .env, *.pyc, __pycache__

### Django Security Settings
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SECURE_HSTS_SECONDS configured (31536000)
- [ ] ALLOWED_HOSTS properly configured
- [ ] DEBUG=False
- [ ] X_FRAME_OPTIONS = 'DENY'
- [ ] SECURE_CONTENT_TYPE_NOSNIFF = True
- [ ] SECURE_BROWSER_XSS_FILTER = True

---

## 📦 DEPENDENCIES

### requirements.txt Verification
- [ ] Django==5.2.15
- [ ] gunicorn==26.0.0 (Production WSGI server)
- [ ] psycopg2-binary==2.9.12 (PostgreSQL adapter)
- [ ] dj-database-url==3.1.2 (Database URL parsing)
- [ ] python-dotenv==1.2.2 (Environment variables)
- [ ] whitenoise==6.12.0 (Static file serving)
- [ ] pillow==12.2.0 (Image handling)
- [ ] No development-only packages (django-debug-toolbar, etc.)

### Missing Packages to Add (if needed)
- [ ] Django-cors-headers (if API accessed from other domains)
- [ ] Django-storages (if using cloud storage for media)
- [ ] Sentry (for error tracking - optional)
- [ ] Redis (for caching - optional)

---

## 🗄️ DATABASE

- [ ] PostgreSQL configured (required for production)
- [ ] DATABASE_URL environment variable set
- [ ] Migrations are all applied: `python manage.py migrate`
- [ ] Database is backed up (Render handles this)
- [ ] Superuser created: `python manage.py createsuperuser`
- [ ] Test connection works

---

## 📂 STATIC & MEDIA FILES

### Static Files Configuration
- [ ] STATIC_ROOT = BASE_DIR / 'staticfiles'
- [ ] STATICFILES_DIRS = [BASE_DIR / 'static']
- [ ] STATIC_URL = '/static/'
- [ ] STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
- [ ] WhiteNoise middleware installed
- [ ] collectstatic runs during build: `python manage.py collectstatic --noinput`
- [ ] All CSS/JS loads correctly in browser
- [ ] Check browser DevTools for 404 errors on assets

### Media Files
- [ ] MEDIA_ROOT properly configured
- [ ] MEDIA_URL properly configured
- [ ] Media files can be uploaded in admin
- [ ] Media files are accessible after upload

---

## 🔧 DEPLOYMENT FILES

- [ ] render.yaml exists and is properly configured
- [ ] Procfile exists as backup
- [ ] Build command in render.yaml: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- [ ] Start command uses gunicorn: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 60`
- [ ] Initial database setup: `python manage.py migrate`

---

## 🧪 LOCAL TESTING

### Pre-Deployment Verification
- [ ] Django check passes: `python manage.py check`
- [ ] Migrations apply cleanly: `python manage.py migrate`
- [ ] Static files collect: `python manage.py collectstatic --noinput`
- [ ] Local server starts: `python manage.py runserver`
- [ ] Admin page loads: http://localhost:8000/admin/
- [ ] Homepage loads and renders correctly
- [ ] All navigation links work
- [ ] Contact form submits and sends email
- [ ] Blog pages display correctly
- [ ] Portfolio pages display correctly
- [ ] No console errors in browser
- [ ] No warnings in Django logs

### Production-Mode Testing (Local)
- [ ] Set DEBUG=False locally
- [ ] Set SECRET_KEY to temporary value
- [ ] Verify collectstatic works
- [ ] Test gunicorn locally: `gunicorn config.wsgi:application`
- [ ] Confirm all pages load
- [ ] Check that static files load in production mode

---

## 📝 GIT & VERSION CONTROL

- [ ] No .env file in git history: `git log --all --full-history --oneline -- .env`
- [ ] .gitignore includes: .env, *.pyc, __pycache__, venv/, .DS_Store, *.sqlite3
- [ ] All code is committed: `git status` shows clean
- [ ] Latest changes pushed to main: `git log -1`
- [ ] No uncommitted changes before deployment
- [ ] Git history is clean (no accidental secret commits)

---

## 🚀 RENDER DEPLOYMENT

### Render Configuration
- [ ] Service name set correctly
- [ ] Runtime: Python 3.12
- [ ] Repository connected to GitHub
- [ ] GitHub branch set to: main
- [ ] Auto-deploy on push enabled
- [ ] Build command configured
- [ ] Start command configured

### Environment Variables in Render
- [ ] SECRET_KEY set and unique
- [ ] DEBUG=False
- [ ] ENVIRONMENT=production
- [ ] DATABASE_URL auto-populated from database
- [ ] EMAIL_HOST_USER set
- [ ] EMAIL_HOST_PASSWORD set
- [ ] ALLOWED_HOSTS includes your domain
- [ ] All values double-checked for typos

### Database on Render
- [ ] PostgreSQL database created
- [ ] Database region same as web service
- [ ] DATABASE_URL connection string verified
- [ ] Initial migration runs on first deploy
- [ ] Database is backed up

---

## ✅ HEALTH CHECKS

### After Deployment
- [ ] Service status shows "Live"
- [ ] No deployment errors in logs
- [ ] Visit https://jamarik-website.onrender.com (or your URL)
- [ ] Homepage loads without errors
- [ ] All pages accessible
- [ ] Admin panel works: /admin/
- [ ] Create superuser and log in
- [ ] Contact form works (test submission)
- [ ] Static files load (CSS, JS, images)
- [ ] No 404 errors in console
- [ ] No 500 errors in logs
- [ ] HTTPS enforced (check URL bar)
- [ ] Security headers present (check browser DevTools)

### Email Verification
- [ ] Test contact form submission
- [ ] Email received in inbox
- [ ] Email formatting looks correct
- [ ] Sender is correct (DEFAULT_FROM_EMAIL)
- [ ] Check spam folder if not received

### Performance Check
- [ ] Page load time acceptable (<3 seconds)
- [ ] Admin panel responsive
- [ ] No timeout errors in logs
- [ ] Database queries are efficient

---

## 📊 MONITORING

### After Going Live
- [ ] Check logs daily for errors
- [ ] Monitor contact form submissions
- [ ] Monitor admin for unusual activity
- [ ] Set up email alerts (optional on paid Render plan)
- [ ] Regular security scans
- [ ] Check disk usage
- [ ] Monitor database size

---

## 🔄 ROLLBACK PLAN

If deployment fails:
- [ ] Render auto-reverts to previous build
- [ ] Check deployment logs for errors
- [ ] Fix issues locally
- [ ] Commit and push again
- [ ] Render auto-redeploys
- [ ] Verify deployment again

---

## 📋 FINAL SIGN-OFF

**Ready for Production?** ✓

Deployment Date: _______________
Deployed By: _______________
Database Backed Up: _______________
Status: [ ] READY [ ] NOT READY - Issue: ________________

---

## ⚠️ IMPORTANT REMINDERS

1. **Never push .env to GitHub**
2. **Always use strong SECRET_KEY**
3. **Keep Django and packages updated**
4. **Monitor logs for security issues**
5. **Regular database backups are critical**
6. **Test changes locally before pushing**
7. **Keep documentation updated**

---

Last Updated: 2026-06-16
Project: Jamarik Technologies Django
Environment: Render.com Production
