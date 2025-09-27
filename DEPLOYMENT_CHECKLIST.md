# Render Deployment Checklist

## ✅ Pre-Deployment Checklist

- [x] **requirements.txt** - Updated with all necessary packages
- [x] **settings.py** - Configured for production with environment variables
- [x] **render.yaml** - Deployment configuration ready
- [x] **build.sh** - Build script with proper permissions and steps
- [x] **start.sh** - Start script with Gunicorn configuration
- [x] **runtime.txt** - Python version specified
- [x] **Static files** - WhiteNoise configured for serving static files
- [x] **Database** - PostgreSQL configuration with dj-database-url
- [x] **Security** - HTTPS redirect and security headers configured

## 📋 Deployment Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Create PostgreSQL Database on Render**
   - Name: rental-system-db
   - Plan: Free

3. **Create Web Service on Render**
   - Runtime: Python 3
   - Build Command: `chmod +x build.sh start.sh && ./build.sh`
   - Start Command: `./start.sh`

4. **Set Environment Variables**
   - DATABASE_URL (from PostgreSQL service)
   - SECRET_KEY (generate secure key)
   - DEBUG = False
   - RENDER = True
   - Other optional variables

5. **Deploy and Monitor**
   - Check build logs
   - Test the application
   - Verify admin access

## 🔧 Post-Deployment

- [ ] Test all major features
- [ ] Verify admin panel access
- [ ] Check static files loading
- [ ] Test database functionality
- [ ] Set up monitoring/alerts
- [ ] Configure custom domain (optional)
- [ ] Set up regular backups

## 📞 Quick Access

- **App URL**: https://your-service-name.onrender.com
- **Admin Panel**: https://your-service-name.onrender.com/admin/
- **Admin Credentials**: 
  - Username: admin
  - Password: [ADMIN_PASSWORD env var or adminpass123]

## 🚨 Troubleshooting

If deployment fails, check:
1. Build logs in Render dashboard
2. Environment variables are set correctly
3. Database connection is established
4. Static files are collected properly
5. Migrations ran successfully