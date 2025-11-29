# Modal App Activity Management

## Current Status

Your `samani-financial-analyst` app is deployed on Modal with NVIDIA A10G GPU support.

**Latest Deployment**: `ap-xeFEodlphRXYUWyrMcSEIV` - **Deployed** ✅

## Why Apps Go Idle

Modal automatically stops inactive apps to save costs. Apps transition to idle state when:
- No requests received for extended period
- Container completes processing and awaits input
- This is **normal** and by design

## Keeping Your App Active

### Option 1: Use Keep-Alive Script (Recommended)

```bash
# Terminal 1: Start keep-alive service (runs in background)
python keep_alive.py 10  # Pings every 10 minutes

# Terminal 2: Use the app normally
python src/main.py
```

The keep-alive script sends periodic test calls to:
- Keep container warm
- Prevent idle shutdown
- Enable instant response time

### Option 2: On-Demand (No Keep-Alive)

Just call the app when needed - Modal will spin it up in seconds:

```python
from modal import App
import modal

app = modal.App.lookup("samani-financial-analyst")
analyzer_cls = app.cls("FinancialAnalyzer")

# This triggers spin-up if idle
result = analyzer_cls.analyze.remote(files, query)
```

### Option 3: Integrate with Gradio

Modify `src/frontend/gradio_app.py` to call Modal API:

```python
import modal

async def process_with_modal(files, query):
    app = modal.App.lookup("samani-financial-analyst")
    analyzer_cls = app.cls("FinancialAnalyzer")
    result, logs = analyzer_cls.analyze.remote(files, query)
    return result
```

## Monitoring

### Check App Status
```bash
modal app list
```

### View App Logs
```bash
modal logs samani-financial-analyst
```

### Check GPU Usage
```bash
modal app logs samani-financial-analyst --level debug
```

## Cost Considerations

| Scenario | Cost |
|----------|------|
| Idle (not running) | $0/hour |
| Running on A10G GPU | $0.40/hour |
| Keep-alive (1 call/10m) | ~$0.07/hour |

**Keep-alive adds ~$0.07/hour** for instant response time.

## Files Provided

- `test_modal_app.py` - Test basic connectivity
- `test_modal_simple.py` - Test with local runner
- `keep_alive.py` - Background keep-alive service
- `modal_server.py` - App with enhanced logging

## Quick Actions

### Reactivate Idle App
```bash
modal deploy src/backend/modal_server.py
```

### View Latest Deployment
```bash
modal app logs ap-xeFEodlphRXYUWyrMcSEIV
```

### Start Keep-Alive (5 min interval)
```bash
python keep_alive.py 5
```

### Stop Keep-Alive
```bash
Ctrl+C
```

## Logs

When app processes requests, logs show:
```
[2025-11-28 19:15:30] 📊 Received analysis request: 2 files
[2025-11-28 19:15:30] ✓ Loaded file: financials_2024.xlsx
[2025-11-28 19:15:32] ⚙️  Processing analysis...
[2025-11-28 19:15:35] ✅ Analysis complete - returning results
```

View live logs:
```bash
modal logs samani-financial-analyst --follow
```

## Troubleshooting

### App Not Responding
1. Check status: `modal app list`
2. Check logs: `modal logs samani-financial-analyst`
3. Redeploy: `modal deploy src/backend/modal_server.py`

### Keep-Alive Not Working
1. Verify authentication: `modal token set`
2. Check connectivity: `modal app list`
3. Test manually: `python test_modal_app.py`

### High Latency
- If app is idle, first call takes 5-10 seconds to spin up
- Use keep-alive for instant response (<1 second)

## Next Steps

1. **For Development**: Use `python src/main.py` locally
2. **For Production**: 
   - Keep `samani-financial-analyst` deployed
   - Use keep-alive script for instant response
   - Or call on-demand (slight delay on first call)
3. **For Monitoring**: Set up `modal logs` in a terminal window

---

**App Ready**: Your Modal deployment is active and ready to handle analysis requests! 🚀
