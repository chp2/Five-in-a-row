# 🚀 GitHub Pages Deployment Guide

This guide will help you deploy your Omok-Lab web game to GitHub Pages.

---

## 📋 Prerequisites

- GitHub account
- Git installed on your computer
- Your Omok-Lab repository

---

## 🎯 Deployment Methods

### Method 1: Automatic Deployment (Recommended)

The repository includes a GitHub Actions workflow that automatically deploys to GitHub Pages when you push to the main branch.

#### Steps:

1. **Push your code to GitHub**:
   ```bash
   cd "c:\changhun\Portfolio\five_row\Five-in-a-row"
   git add .
   git commit -m "Add web version of Omok-Lab"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under "Build and deployment":
     - Source: **GitHub Actions**
   - Save

3. **Wait for deployment**:
   - Go to **Actions** tab
   - Watch the deployment workflow run
   - Once complete, your site will be live!

4. **Access your game**:
   ```
   https://[your-username].github.io/Five-in-a-row/
   ```

---

### Method 2: Manual Deployment

If you prefer manual deployment without GitHub Actions:

#### Steps:

1. **Push your code to GitHub**:
   ```bash
   cd "c:\changhun\Portfolio\five_row\Five-in-a-row"
   git add .
   git commit -m "Add web version of Omok-Lab"
   git push origin main
   ```

2. **Configure GitHub Pages**:
   - Go to **Settings** → **Pages**
   - Under "Build and deployment":
     - Source: **Deploy from a branch**
     - Branch: **main**
     - Folder: **/web**
   - Click **Save**

3. **Wait for deployment** (~1-2 minutes)

4. **Access your game**:
   ```
   https://[your-username].github.io/Five-in-a-row/
   ```

---

## 🌐 Custom Domain (Optional)

Want to use your own domain? Follow these steps:

### 1. Add CNAME file

Create a file named `CNAME` in the `web` folder:
```
yourdomain.com
```

### 2. Configure DNS

At your domain registrar, add these DNS records:

**For apex domain (example.com):**
```
Type: A
Name: @
Value: 185.199.108.153
Value: 185.199.109.153
Value: 185.199.110.153
Value: 185.199.111.153
```

**For www subdomain:**
```
Type: CNAME
Name: www
Value: [your-username].github.io
```

### 3. Enable in GitHub

- Go to **Settings** → **Pages**
- Enter your custom domain
- Check **Enforce HTTPS**
- Save

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Game board loads correctly
- [ ] Stones can be placed by clicking
- [ ] AI moves work
- [ ] Forbidden moves show red X marks
- [ ] Move history updates
- [ ] All buttons function properly
- [ ] Responsive design works on mobile

---

## 🐛 Troubleshooting

### Issue: 404 Page Not Found

**Solution:**
- Check that the `web` folder is in your repository
- Verify GitHub Pages source is set to `/web` folder
- Wait a few minutes for deployment to complete

### Issue: Styles not loading

**Solution:**
- Ensure `styles.css` is in the same folder as `index.html`
- Check browser console for errors
- Clear browser cache (Ctrl+F5)

### Issue: JavaScript errors

**Solution:**
- Ensure `game.js` is in the same folder as `index.html`
- Check browser console for specific errors
- Verify all files were uploaded correctly

### Issue: AI is slow

**Solution:**
- This is normal for higher difficulty levels
- Reduce AI difficulty in settings
- Consider optimizing the minimax algorithm

---

## 📊 Analytics (Optional)

Want to track visitors? Add Google Analytics:

1. Get your GA4 tracking ID
2. Add to `index.html` before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🔒 Security

GitHub Pages is secure by default:
- ✅ HTTPS enabled automatically
- ✅ No server-side code execution
- ✅ Static files only
- ✅ DDoS protection included

---

## 📈 Performance Tips

1. **Enable Caching**: GitHub Pages automatically caches static files
2. **Optimize Images**: If you add images, compress them first
3. **Minify Code**: For production, consider minifying CSS/JS
4. **Use CDN**: GitHub Pages uses a global CDN automatically

---

## 🎨 Customization After Deployment

You can customize the game even after deployment:

1. **Edit files locally**
2. **Test changes** by opening `index.html` in browser
3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Update game design"
   git push origin main
   ```
4. **Wait for auto-deployment** (~1 minute)

---

## 📞 Support

If you encounter issues:

1. Check the [GitHub Pages documentation](https://docs.github.com/en/pages)
2. Review browser console for errors
3. Test locally first before deploying
4. Check GitHub Actions logs for deployment errors

---

## 🎉 Success!

Once deployed, share your game:

```
🎮 Play Omok-Lab: https://[your-username].github.io/Five-in-a-row/
```

Share on:
- Twitter/X
- LinkedIn
- Reddit
- Your portfolio website

---

<div align="center">

**Happy Gaming! ⚫⚪**

Made with ❤️ using GitHub Pages

</div>
