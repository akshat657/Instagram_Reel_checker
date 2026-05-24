# Deployment Guide

Deploy MedReel Analyzer with **Vercel (Frontend) + Render (Backend) + GitHub Actions (Keep-Awake Cron)**

## Prerequisites

- GitHub account
- Vercel account (free - sign up at https://vercel.com)
- Render account (free - sign up at https://render.com)
- API keys ready:
  - 3x Groq API keys (https://console.groq.com/keys)
  - 1x RapidAPI key (https://rapidapi.com/)

---

## Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Deploy: FastAPI + React MedReel Analyzer"

# Create new GitHub repo at https://github.com/new
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/Instagram_reel_buster.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Render

### 2.1 Connect GitHub Repository

1. Go to https://dashboard.render.com
2. Click **New +** → **Blueprint**
3. Connect your GitHub repository: `Instagram_reel_buster`
4. Render will detect `render.yaml` automatically
5. Click **Apply**

### 2.2 Add Environment Variables

In Render dashboard → **medreel-backend** → **Environment**:

```
GROQ_API_KEY_1=gsk_...
GROQ_API_KEY_2=gsk_...
GROQ_API_KEY_3=gsk_...
RAPIDAPI_KEY=...
```

### 2.3 Manual Deploy (if needed)

Click **Manual Deploy** → **Deploy latest commit**

### 2.4 Get Backend URL

Once deployed, copy your backend URL:
```
https://medreel-backend.onrender.com
```

**Note:** First deploy takes 5-10 minutes. Subsequent deploys are faster.

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Import Project

1. Go to https://vercel.com/new
2. Click **Import Git Repository**
3. Select: `YOUR_USERNAME/Instagram_reel_buster`
4. **Root Directory**: `frontend` ⚠️ **IMPORTANT**
5. **Framework Preset**: Vite
6. **Build Command**: `npm run build`
7. **Output Directory**: `dist`

### 3.2 Add Environment Variable

In **Environment Variables** section:

```
VITE_API_URL=https://medreel-backend.onrender.com
```

(Use the backend URL from Step 2.4)

### 3.3 Deploy

Click **Deploy** → Wait 2-3 minutes

### 3.4 Get Frontend URL

Copy your frontend URL:
```
https://medreel-analyzer.vercel.app
```

---

## Step 4: Update Backend CORS

### 4.1 Add Frontend URL to CORS

In Render dashboard → **medreel-backend** → **Environment**:

Add/update:
```
CORS_ORIGINS=["https://medreel-analyzer.vercel.app"]
```

(Replace with your actual Vercel URL)

### 4.2 Redeploy Backend

Click **Manual Deploy** to apply CORS changes

---

## Step 5: Enable Keep-Awake Cron Job

### 5.1 Update Cron Job URL

Edit `.github/workflows/keep-backend-awake.yml`:

Line 15: Replace with your Render backend URL:
```yaml
response=$(curl -s -o /dev/null -w "%{http_code}" https://medreel-backend.onrender.com/api/health)
```

### 5.2 Push to GitHub

```bash
git add .github/workflows/keep-backend-awake.yml
git commit -m "Update cron job with backend URL"
git push
```

### 5.3 Verify Cron Job

1. Go to GitHub → **Actions** tab
2. You should see "Keep Backend Awake" workflow
3. Click **Run workflow** to test manually
4. It will auto-run every 10 minutes

---

## Step 6: Test Deployment

1. **Open Frontend**: https://medreel-analyzer.vercel.app
2. **Paste Instagram URL**: `https://www.instagram.com/reel/DRw-9YTEfQs/`
3. **Click Analyze**
4. **Wait for Results** (first request may take 30-60s as backend wakes up)

---

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed on Render
- [ ] Environment variables added on Render
- [ ] Backend health check returns 200: `https://YOUR-BACKEND.onrender.com/api/health`
- [ ] Frontend deployed on Vercel
- [ ] `VITE_API_URL` set on Vercel
- [ ] Backend CORS updated with Vercel URL
- [ ] Cron job updated with backend URL
- [ ] Test analysis with real Instagram Reel

---

## Monitoring

### Backend Logs (Render)
https://dashboard.render.com → **medreel-backend** → **Logs**

### Frontend Logs (Vercel)
https://vercel.com → **Your Project** → **Deployments** → **View Function Logs**

### Cron Job Logs (GitHub)
https://github.com/YOUR_USERNAME/Instagram_reel_buster → **Actions**

---

## Troubleshooting

### Backend sleeps after 15 minutes
- ✅ Ensure GitHub Actions cron job is enabled
- ✅ Check Actions tab for successful runs
- ✅ Verify cron URL matches your backend

### CORS errors
- ✅ Add Vercel URL to `CORS_ORIGINS` on Render
- ✅ Redeploy backend after changing CORS

### Frontend shows "Network Error"
- ✅ Check `VITE_API_URL` on Vercel matches Render backend
- ✅ Test backend health: `https://YOUR-BACKEND.onrender.com/api/health`

### Analysis fails
- ✅ Check Groq API keys are valid on Render
- ✅ Check RapidAPI key is valid
- ✅ View backend logs on Render for errors

---

## Custom Domain (Optional)

### Frontend (Vercel)
1. Vercel Dashboard → **Domains**
2. Add your domain: `medreel.yourdomain.com`
3. Follow DNS instructions

### Backend (Render)
1. Render Dashboard → **Settings** → **Custom Domain**
2. Add: `api.yourdomain.com`
3. Update `VITE_API_URL` on Vercel
4. Update CORS on Render

---

## Cost Estimate

- **Vercel (Frontend)**: $0/month (free tier, unlimited bandwidth)
- **Render (Backend)**: $0/month (free tier, 750 hours/month with cron keepalive)
- **GitHub Actions**: $0/month (2000 minutes/month free, cron uses ~5 min/month)

**Total: $0/month** 🎉

---

## Upgrading to Paid (Optional)

If you exceed free tier limits:

- **Render Pro**: $7/month (no sleep, faster)
- **Vercel Pro**: $20/month (more bandwidth, better analytics)

Free tier is sufficient for moderate usage (100-1000 analyses/day).
