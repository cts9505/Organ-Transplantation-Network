# 🚀 Serverless Deployment Guide

This application can be deployed to multiple serverless platforms. Choose the one that best fits your needs!

---

## 📋 Table of Contents

1. [Vercel (Recommended for Quick Deploy)](#vercel)
2. [Netlify](#netlify)
3. [Railway](#railway)
4. [Render](#render)
5. [Heroku](#heroku)
6. [AWS Lambda](#aws-lambda)
7. [Google Cloud Run](#google-cloud-run)
8. [Azure App Service](#azure-app-service)
9. [Docker (Self-hosted)](#docker)
10. [Database Setup](#database-setup)

---

## 🌐 Vercel

### Prerequisites
- GitHub/GitLab account
- Vercel account (free tier available)
- MySQL database (PlanetScale, AWS RDS, or Railway recommended)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/organ-transplant-network.git
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository
   - Vercel will auto-detect `vercel.json`

3. **Set Environment Variables**
   In Vercel dashboard → Settings → Environment Variables:
   ```
   DB_HOST=your-database-host
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_NAME=DBMS_PROJECT
   FLASK_SECRET_KEY=your-random-secret-key
   FLASK_DEBUG=False
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy automatically
   - Your app will be live at `https://your-project.vercel.app`

### Database Recommendations for Vercel
- **PlanetScale** (MySQL-compatible, serverless) - Recommended
- **Railway** (Free tier includes MySQL)
- **AWS RDS** (Production-ready)

---

## 🎨 Netlify

### Deployment Steps

1. **Push to GitHub** (same as Vercel)

2. **Deploy to Netlify**
   ```bash
   npm install -g netlify-cli
   netlify login
   netlify init
   netlify deploy --prod
   ```

   Or use Netlify UI:
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Select your repository

3. **Set Environment Variables**
   In Netlify dashboard → Site settings → Environment variables

4. **Install Serverless WSGI**
   Add to `requirements.txt`:
   ```
   serverless-wsgi
   ```

---

## 🚂 Railway

### Deployment Steps (Easiest for beginners!)

1. **Deploy with One Click**
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Initialize project
   railway init
   
   # Add MySQL
   railway add
   # Select "MySQL"
   
   # Deploy
   railway up
   ```

2. **Environment Variables**
   Railway automatically sets MySQL variables:
   - `MYSQL_URL` is auto-configured
   - Add `FLASK_SECRET_KEY` manually

3. **Access Your App**
   - Railway generates a public URL
   - Or add custom domain in settings

### Railway.toml
Already configured! Just run `railway up`

---

## 🎯 Render

### Deployment Steps

1. **Connect GitHub**
   - Go to [render.com](https://render.com)
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   Render will auto-detect `render.yaml`:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`

3. **Add Database**
   - Create a PostgreSQL or MySQL database on Render
   - Or use external MySQL (Railway, PlanetScale)

4. **Set Environment Variables**
   Add in Render dashboard

5. **Deploy**
   - Click "Create Web Service"
   - Automatic deploys on git push!

---

## 💜 Heroku

### Deployment Steps

1. **Install Heroku CLI**
   ```bash
   brew install heroku/brew/heroku
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create organ-transplant-network
   ```

3. **Add MySQL Addon**
   ```bash
   # ClearDB (free tier)
   heroku addons:create cleardb:ignite
   
   # Get database URL
   heroku config:get CLEARDB_DATABASE_URL
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set FLASK_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
   heroku config:set FLASK_DEBUG=False
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open App**
   ```bash
   heroku open
   ```

---

## ☁️ AWS Lambda

### Prerequisites
- AWS Account
- AWS CLI configured
- Zappa or Serverless Framework

### Using Zappa

1. **Install Zappa**
   ```bash
   pip install zappa
   ```

2. **Initialize**
   ```bash
   zappa init
   ```

3. **Create zappa_settings.json** (already provided!)

4. **Deploy**
   ```bash
   zappa deploy dev
   ```

5. **Update**
   ```bash
   zappa update dev
   ```

### Database for AWS Lambda
- **AWS RDS MySQL** (Best integration)
- **AWS Aurora Serverless** (Auto-scaling)
- Configure VPC settings in `zappa_settings.json`

---

## 🐳 Docker (Self-hosted)

### Local Development

1. **Build and Run**
   ```bash
   docker-compose up --build
   ```

2. **Access App**
   - App: http://localhost:8080
   - MySQL: localhost:3306

3. **Stop Services**
   ```bash
   docker-compose down
   ```

### Production Deployment

```bash
# Build image
docker build -t organ-transplant-network .

# Run container
docker run -d \
  -p 8080:8080 \
  -e DB_HOST=your-db-host \
  -e DB_USER=your-db-user \
  -e DB_PASSWORD=your-db-password \
  -e DB_NAME=DBMS_PROJECT \
  -e FLASK_SECRET_KEY=your-secret-key \
  organ-transplant-network
```

### Deploy to Cloud Platforms

**Google Cloud Run:**
```bash
gcloud run deploy organ-transplant \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**AWS ECS/Fargate:**
```bash
aws ecr create-repository --repository-name organ-transplant
docker tag organ-transplant-network:latest <ecr-url>
docker push <ecr-url>
```

**Azure Container Instances:**
```bash
az container create \
  --resource-group myResourceGroup \
  --name organ-transplant \
  --image organ-transplant-network \
  --ports 8080
```

---

## 💾 Database Setup

### Option 1: PlanetScale (Recommended for Serverless)

1. **Create Database**
   - Go to [planetscale.com](https://planetscale.com)
   - Create free database
   - Get connection string

2. **Import Schema**
   ```bash
   pscale shell organ-transplant main < create_tables_fixed.sql
   ```

3. **Import Data**
   ```bash
   pscale shell organ-transplant main < inserting_data/complete_demo_data.sql
   ```

### Option 2: Railway MySQL

1. **Add MySQL Service**
   ```bash
   railway add
   # Select MySQL
   ```

2. **Get Connection Details**
   ```bash
   railway variables
   ```

3. **Import Schema**
   ```bash
   mysql -h <host> -u <user> -p<password> DBMS_PROJECT < create_tables_fixed.sql
   ```

### Option 3: AWS RDS

1. **Create RDS Instance**
   - Go to AWS RDS Console
   - Create MySQL 8.0 instance
   - Configure security groups

2. **Connect and Import**
   ```bash
   mysql -h <rds-endpoint> -u admin -p < create_tables_fixed.sql
   ```

### Option 4: Google Cloud SQL

```bash
gcloud sql instances create organ-transplant-db \
  --database-version=MYSQL_8_0 \
  --tier=db-f1-micro \
  --region=us-central1

gcloud sql databases create DBMS_PROJECT --instance=organ-transplant-db
```

---

## 🔑 Environment Variables Reference

All platforms need these environment variables:

```env
DB_HOST=your-database-host
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_NAME=DBMS_PROJECT
FLASK_SECRET_KEY=your-random-secret-key-min-32-chars
FLASK_DEBUG=False
```

### Generate Secret Key
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## ✅ Platform Comparison

| Platform | Free Tier | Auto-Deploy | Database Included | Best For |
|----------|-----------|-------------|-------------------|----------|
| **Vercel** | ✅ Yes | ✅ Yes | ❌ No | Static + Serverless |
| **Netlify** | ✅ Yes | ✅ Yes | ❌ No | JAMstack apps |
| **Railway** | ✅ Yes ($5 credit) | ✅ Yes | ✅ Yes | Full-stack apps |
| **Render** | ✅ Yes | ✅ Yes | ✅ Yes (paid) | Production apps |
| **Heroku** | ⚠️ Limited | ✅ Yes | ⚠️ Addon | Legacy apps |
| **AWS Lambda** | ✅ Yes | ❌ Manual | ❌ No | Scalability |
| **Docker** | N/A | ❌ Manual | ✅ Self-hosted | Full control |

---

## 🚀 Quick Start Recommendations

### For Beginners
👉 **Railway** - Easiest setup with built-in database

### For Free Hosting
👉 **Vercel + PlanetScale** - Best free tier combo

### For Production
👉 **Render** or **AWS Lambda** - Professional grade

### For Full Control
👉 **Docker + VPS** - Complete flexibility

---

## 🔧 Troubleshooting

### Connection Timeout
- Check database firewall rules
- Verify VPC configuration (for AWS Lambda)
- Ensure database allows external connections

### Import Errors
```bash
# Install missing dependencies
pip install -r requirements.txt
```

### Database Connection Errors
- Verify environment variables
- Check database is running
- Test connection string manually

---

## 📚 Additional Resources

- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Vercel Python Guide](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Railway Deployment Docs](https://docs.railway.app/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 💡 Tips

1. **Always use environment variables** for sensitive data
2. **Enable HTTPS** on production (most platforms do this automatically)
3. **Use database connection pooling** for better performance
4. **Monitor your app** with platform analytics
5. **Set up CI/CD** for automated deployments

---

**Need Help?** Check platform-specific documentation or open an issue!
