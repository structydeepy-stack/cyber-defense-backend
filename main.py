from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime

app = FastAPI(title="STRUCTY_DEEPY DEFENSE CORE")

logs = []

def add_log(message: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}"
    logs.append(entry)
    print(entry)

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DEFENSE OPERATIONS CENTER</title>
    <style>
        :root {
            --neon-red: #ff0044;
            --neon-cyan: #00ffff;
            --neon-green: #00ff88;
            --blood: #8b0000;
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: #0a0005;
            color: #ddd;
            font-family: 'Courier New', monospace;
            overflow-x: hidden;
        }
        .scanline {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: linear-gradient(transparent 50%, rgba(0,255,70,0.03) 50%);
            background-size: 100% 4px;
            pointer-events: none;
            animation: scan 4s linear infinite;
            z-index: 1;
            opacity: 0.6;
        }
        @keyframes scan { 0% {transform:translateY(-100%);} 100% {transform:translateY(100%);} }
        
        .glitch {
            position: relative;
            color: var(--neon-red);
            font-weight: bold;
            animation: glitch-skew 4s infinite linear alternate-reverse;
        }
        .neon-red { color: var(--neon-red); text-shadow: 0 0 10px var(--neon-red), 0 0 20px var(--neon-red); }
        .neon-cyan { color: var(--neon-cyan); text-shadow: 0 0 10px var(--neon-cyan), 0 0 20px var(--neon-cyan); }
        .neon-green { color: var(--neon-green); text-shadow: 0 0 10px var(--neon-green), 0 0 20px var(--neon-green); }
        
        .container { max-width: 1100px; margin: 0 auto; padding: 20px; position: relative; z-index: 2; }
        .log {
            background: #050000;
            border: 2px solid var(--neon-red);
            padding: 20px;
            height: 65vh;
            overflow-y: auto;
            white-space: pre-wrap;
            box-shadow: 0 0 25px var(--neon-red);
            font-size: 1.1rem;
        }
        .alert { color: #ff0044; animation: flash 1s infinite; }
        @keyframes flash { 50% {opacity: 0.3;} }
        
        header { text-align: center; padding: 20px; border-bottom: 3px solid #8b0000; }
        .warning-banner {
            background: linear-gradient(90deg, #ff0000, #ff8800);
            color: #000;
            padding: 12px;
            font-weight: bold;
            margin: 15px 0;
            animation: glitch 1s infinite;
        }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container">
        <header>
            <h1 class="glitch" data-text="DEFENSE OPERATIONS CENTER">DEFENSE OPERATIONS CENTER</h1>
            <div class="warning-banner">THREAT LEVEL: CRITICAL — PERSISTENT PYNCAT DETECTED</div>
        </header>
        
        <div class="log" id="log"></div>
    </div>

    <script>
        async function fetchLogs() {
            const res = await fetch('/logs');
            const text = await res.text();
            document.getElementById('log').textContent = text;
            document.getElementById('log').scrollTop = 999999;
        }
        setInterval(fetchLogs, 800);
        fetchLogs();
    </script>
</body>
</html>"""

@app.get("/logs")
async def get_logs():
    return "\n".join(logs[-100:])

@app.post("/attack")
async def register_attack(request: Request):
    data = await request.json()
    add_log(f"🚨 PyNcat CONNECTION ATTEMPT from {request.client.host}", "CRITICAL")
    add_log(f"SSL: {data.get('ssl', False)} | Persistent: {data.get('persistent', False)}", "ALERT")
    add_log("Self-signed certificate detected → /tmp/pyncat_cert.pem", "WARNING")
    add_log("Exponential backoff reconnection detected", "WARNING")
    add_log("✅ EDR BLOCKED the reverse shell", "SUCCESS")
    return {"status": "contained"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
