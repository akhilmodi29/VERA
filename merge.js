const fs = require('fs');
let prefix = fs.readFileSync('frontend/src/pages/Dashboard_prefix.txt', 'utf8');
let suffix = fs.readFileSync('frontend/src/pages/Dashboard_suffix.txt', 'utf8');
fs.writeFileSync('frontend/src/pages/Dashboard.tsx', prefix + suffix);
