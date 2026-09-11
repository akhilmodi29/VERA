const fs = require('fs');
let c = fs.readFileSync('frontend/src/pages/Dashboard.tsx', 'utf8');

c = c.replace(/const ra = riskRes\.data\.risk_analysis;/g, \const ra = riskRes.data.risk_analysis as {
        overall_risk_score: number;
        risk_level: string;
        contributing_signals: string[];
        confidence?: number;
        voice_integrity_score?: number;
        voice_label?: string;
        voice_confidence?: number;
        speaker_similarity_score?: number | null;
      };\);

c = c.replace(/const STAGE_LABELS: Record<AnalysisStage, string> = {/g, "// const STAGE_LABELS: Record<AnalysisStage, string> = {");
c = c.replace(/idle: '',/g, "// idle: '',");
c = c.replace(/decoding: 'Decoding audio...',/g, "// decoding: 'Decoding audio...',");
c = c.replace(/voice: 'Analyzing voice integrity...',/g, "// voice: 'Analyzing voice integrity...',");
c = c.replace(/speech: 'Transcribing speech...',/g, "// speech: 'Transcribing speech...',");
c = c.replace(/risk: 'Calculating risk score...',/g, "// risk: 'Calculating risk score...',");
c = c.replace(/policy: 'Evaluating policy...',/g, "// policy: 'Evaluating policy...',");
c = c.replace(/done: 'Analysis complete.',/g, "// done: 'Analysis complete.',");
c = c.replace(/error: 'Analysis failed.',/g, "// error: 'Analysis failed.',");
c = c.replace(/};\r?\nconst Dashboard: React\.FC = \(\) => {/g, "// };\nconst Dashboard: React.FC = () => {");

fs.writeFileSync('frontend/src/pages/Dashboard.tsx', c);
