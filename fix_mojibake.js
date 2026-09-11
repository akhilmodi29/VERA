const fs = require('fs');
let c = fs.readFileSync('frontend/src/layouts/MainLayout.tsx', 'utf8');
c = c.replace(/Detect.*Protect/g, "Detect • Verify • Protect");
fs.writeFileSync('frontend/src/layouts/MainLayout.tsx', c);
