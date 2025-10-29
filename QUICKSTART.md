# Quick Start Guide - YouTube API Server with Webshare Proxy

## ✅ Setup Complete!

Your server is configured and ready to use with Webshare rotating proxies.

## Start the Server

```bash
cd /Users/reza/Desktop/MASTER/Projects/BACKENDS/uvi-yt
source venv/bin/activate
python run.py
```

Server will be available at: **http://localhost:8000**

## Test the Setup

```bash
# Run the test suite
source venv/bin/activate
python test_proxy.py
```

Expected output:
```
🎉 All tests passed! Server is ready to use with Webshare proxy.
```

## Try It Out

Once the server is running, visit:
- 📚 **API Docs**: http://localhost:8000/docs
- 📖 **Alternative Docs**: http://localhost:8000/redoc

### Example: Get Video Captions

```bash
curl -X POST "http://localhost:8000/youtube/video-captions" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=PLKrSVuT-Dg"}'
```

### Example: Get Video Timestamps

```bash
curl -X POST "http://localhost:8000/youtube/video-timestamps" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=PLKrSVuT-Dg"}'
```

## What's Configured

✅ Webshare proxy credentials loaded  
✅ Proxy type set to `webshare`  
✅ All YouTube transcript requests route through proxy  
✅ Virtual environment set up with all dependencies  
✅ Test suite created and verified  

## Files Created/Modified

- `.env` - Your active configuration with credentials
- `.envrc` - direnv configuration with proxy settings
- `test_proxy.py` - Test suite to verify proxy functionality
- `PROXY_SETUP.md` - Detailed documentation

## Need Help?

See `PROXY_SETUP.md` for detailed documentation and troubleshooting.
