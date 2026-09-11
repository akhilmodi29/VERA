const fs = require('fs');
let c = fs.readFileSync('frontend/src/pages/Dashboard.tsx', 'utf8');

if (!c.includes('Users,')) {
  c = c.replace(/import \{([\s\S]*?)\} from 'lucide-react';/, (match, group) => {
      return "import {" + group + ", Users, ChevronRight} from 'lucide-react';";
  });
}

c = c.replace(/displayRiskData\?\.confidence \?/g, "false ?");
c = c.replace(/evidenceData\.hash\.substring/g, "(evidenceData?.hash || '').substring");

c = c.replace(/const STAGE_LABELS: Record<AnalysisStage, string> = {[\s\S]*?};/g, "/* STAGE_LABELS */");
c = c.replace(/recordingTime,/g, "/* recordingTime, */");
c = c.replace(/startRecording,/g, "/* startRecording, */");
c = c.replace(/stopRecording,/g, "/* stopRecording, */");
c = c.replace(/const formatTime = \([\s\S]*?};/g, "/* formatTime */");
c = c.replace(/const handleRunAnalysis = async \(\) => {[\s\S]*?setAnalysisStage\('error'\);\r?\n    }\r?\n  };/g, "/* handleRunAnalysis */");

c = c.replace(/const isProcessing =[\s\S]*?;/g, "/* isProcessing */");
c = c.replace(/const isMicActive =[\s\S]*?Processing';/g, "/* isMicActive */");

fs.writeFileSync('frontend/src/pages/Dashboard.tsx', c);
