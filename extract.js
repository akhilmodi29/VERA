const fs = require('fs');
let content = fs.readFileSync('frontend/src/pages/Dashboard.tsx', 'utf8');
let prefix = content.split('  return (')[0];
fs.writeFileSync('frontend/src/pages/Dashboard_prefix.txt', prefix);
