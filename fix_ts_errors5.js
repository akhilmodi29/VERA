const fs = require('fs');
let c = fs.readFileSync('frontend/src/pages/Dashboard.tsx', 'utf8');

c = c.replace(/console\.log\(isRecording, audioBlob\);/g, "");
c = c.replace(/isRecording,/g, "/* isRecording, */");
c = c.replace(/audioBlob,/g, "/* audioBlob, */");

fs.writeFileSync('frontend/src/pages/Dashboard.tsx', c);
