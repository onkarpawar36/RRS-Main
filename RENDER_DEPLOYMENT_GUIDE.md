# Render.com Deployment Guide for Django Rental System

This guide will help you deploy your Django Rental System to Render.com.

## Prerequisites

1. A GitHub account with your code pushed to a repository
2. A Render.com account (free tier available)

## Deployment Steps

### 1. Prepare Your Repository

Make sure all the updated files are committed and pushed to your GitHub repository:

```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

### 2. Create a New Web Service on Render

1. Log in to [Render.com](https://render.com)
2. Click "New +" button and select "Web Service"
3. Connect your GitHub repository containing the rental system code
4. Configure the web service:

   **Basic Settings:**
   - Name: `rental-system` (or your preferred name)
   - Runtime: `Python 3`
   - Build Command: `chmod +x build.sh start.sh && ./build.sh`
   - Start Command: `./start.sh`

### 3. Create PostgreSQL Database

1. In your Render dashboard, click "New +" and select "PostgreSQL"
2. Configure the database:
   - Name: `rental-system-db`
   - Database Name: `rental_system`
   - User: `rental_system_user`
   - Plan: Free (or your preferred plan)

3. Wait for the database to be created and note the connection details

### 4. Configure Environment Variables

In your Web Service settings, add these environment variables:

**Required Environment Variables:**

| Key | Value | Notes |
|-----|--------|-------|
| `DATABASE_URL` | (Auto-generated from your PostgreSQL service) | Link to your database |
| `SECRET_KEY` | (Generate a secure secret key) | Use Render's "Generate Value" feature |
| `DEBUG` | `False` | Always False in production |
| `RENDER` | `True` | Identifies Render environment |
| `DJANGO_SETTINGS_MODULE` | `rental_system_project.settings` | Points to settings file |
| `PYTHON_VERSION` | `3.11.0` | Python version to use |
| `WEB_CONCURRENCY` | `4` | Number of worker processes |
| `DJANGO_LOG_LEVEL` | `INFO` | Logging level |

**Optional Environment Variables:**

| Key | Value | Notes |
|-----|--------|-------|
| `ADMIN_PASSWORD` | (Your choice) | Password for auto-created admin user |

### 5. Link Database to Web Service

1. In your Web Service environment variables, set `DATABASE_URL` to reference your PostgreSQL database:
   - Key: `DATABASE_URL`
   - Value: Select "From Database" → Choose your PostgreSQL service → Connection String

### 6. Deploy

1. Click "Create Web Service" or "Deploy Latest Commit"
2. Monitor the build logs for any errors
3. The build process will:
   - Install Python dependencies
   - Collect static files
   - Run database migrations
   - Create an admin user (if configured)

### 7. Access Your Application

Once deployment is complete:

1. Your app will be available at: `https://your-service-name.onrender.com`
2. Admin panel: `https://your-service-name.onrender.com/admin/`
   - Username: `admin`
   - Password: Value of `ADMIN_PASSWORD` environment variable (or `adminpass123` if not set)

## Deployment Using render.yaml (Alternative Method)

If you prefer using the `render.yaml` file for deployment:

1. Make sure your `render.yaml` file is in the repository root
2. In Render dashboard, when creating services, choose "Deploy from YAML"
3. Connect your repository and Render will automatically create both the web service and database

## Troubleshooting

### Common Issues and Solutions:

1. **Build Fails with Permission Errors**
   - Solution: The build script includes `chmod +x build.sh start.sh` to fix permissions

2. **Static Files Not Loading**
   - Check that `STATIC_ROOT` and `STATIC_URL` are correctly set
   - Verify WhiteNoise is in `MIDDLEWARE` and properly configured
   - Ensure `collectstatic` runs during build

3. **Database Connection Errors**
   - Verify `DATABASE_URL` environment variable is correctly linked
   - Check that PostgreSQL service is running
   - Ensure database migrations ran successfully

4. **HTTPS Redirect Issues**
   - Check `SECURE_SSL_REDIRECT` and `SECURE_PROXY_SSL_HEADER` settings
   - Verify `ALLOWED_HOSTS` includes your Render hostname

### Viewing Logs:

1. Go to your Web Service dashboard
2. Click on "Logs" tab to view real-time logs
3. Check for any error messages during startup

### Updating Your Application:

1. Push changes to your GitHub repository
2. Render will automatically detect changes and redeploy
3. Or manually trigger deployment from Render dashboard

## Production Considerations

1. **Database Backups**: Set up regular backups in your PostgreSQL service settings
2. **Domain Name**: Configure a custom domain in your Web Service settings if needed
3. **Environment Variables**: Store sensitive data in environment variables, never in code
4. **Monitoring**: Use Render's monitoring features to track performance
5. **Scaling**: Upgrade to paid plans for better performance and features

## Security Notes

- Never commit sensitive information like secret keys or passwords to your repository
- Use environment variables for all configuration
- The application is configured with HTTPS redirect and security headers for production
- Regularly update dependencies to patch security vulnerabilities

## Support

If you encounter issues:

1. Check Render's [documentation](https://render.com/docs)
2. Review the build and runtime logs for error messages
3. Ensure all environment variables are correctly set
4. Verify your GitHub repository has all necessary files

Your Django Rental System is now ready for deployment on Render.com!