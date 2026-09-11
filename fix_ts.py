import re

with open('frontend/src/pages/Dashboard.tsx', 'r') as f:
    c = f.read()

# Fix connection states
c = c.replace("'disconnected'", "'Disconnected'")
c = c.replace("'connecting'", "'Connecting'")
c = c.replace("'connected'", "'Connected'")
c = c.replace("'live'", "'Live'")
c = c.replace("'processing'", "'Processing'")

# Fix startLiveDetection call
c = c.replace("onClick={startLiveDetection}", "onClick={() => activeSession && startLiveDetection(activeSession.session_id)}")

# Fix analysisStage error by casting
c = c.replace("analysisStage !== 'idle'", "(analysisStage as string) !== 'idle'")

with open('frontend/src/pages/Dashboard.tsx', 'w') as f:
    f.write(c)
