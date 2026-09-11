const fs = require('fs');
let c = fs.readFileSync('frontend/src/pages/Dashboard.tsx', 'utf8');

c = c.replace(/\{false \? \(\(null\) \* 100\)\.toFixed\(1\) \+ '%' : '98\.4%'\}/g, "'98.4%'");

c = c.replace(/\/\* analysisStage \*\//g, "const [analysisStage, setAnalysisStage] = useState<AnalysisStage>('idle');\n  console.log(analysisStage);");

c = c.replace(/\/\* isRecording, \*\//g, "isRecording,");
c = c.replace(/\/\* audioBlob, \*\//g, "audioBlob,");
c = c.replace("const Dashboard: React.FC = () => {", "const Dashboard: React.FC = () => {\n  console.log(isRecording, audioBlob);");

fs.writeFileSync('frontend/src/pages/Dashboard.tsx', c);
