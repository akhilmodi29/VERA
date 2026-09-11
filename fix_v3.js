const fs = require('fs');
let c = fs.readFileSync('frontend/src/pages/Dashboard.tsx', 'utf8');

c = c.replace(/\/\* handleRunAnalysis \*\//g, `  const handleRunAnalysis = async (blob: Blob) => {
    if (!activeSession) return;
    setBatchRisk(null);
    setBatchDecision(null);
    setDecisionError(null);
    setEvidenceData(null);
    setError(null);
    setAnalysisStage('decoding');
    try {
      setAnalysisStage('voice');
      let riskRes;
      try {
        riskRes = await api.analyzeRisk(activeSession.session_id, blob);
      } catch (riskErr) {
        setError(riskErr instanceof Error ? riskErr.message : 'Risk analysis failed.');
        setAnalysisStage('error');
        return;
      }
      const ra = riskRes.data.risk_analysis;
      const extractedRisk = {
        overall_risk_score: ra.overall_risk_score,
        risk_level: ra.risk_level,
        contributing_signals: ra.contributing_signals ?? [],
        confidence: ra.confidence,
        voice_integrity_score: ra.voice_integrity_score,
        voice_label: ra.voice_label,
        voice_confidence: ra.voice_confidence,
        speaker_similarity_score: ra.speaker_similarity_score ?? null,
        transcript: riskRes.data.transcript ?? '',
      };
      setBatchRisk(extractedRisk);
      setAnalysisStage('policy');
      try {
        const decisionRes = await api.getDecision(activeSession.session_id, blob);
        setBatchDecision(decisionRes.data.policy);
      } catch (decErr) {
        setDecisionError(decErr instanceof Error ? decErr.message : 'Policy decision unavailable.');
      }
      try {
        const evidenceRes = await api.generateEvidence(activeSession.session_id, blob);
        if (evidenceRes?.data) setEvidenceData(evidenceRes.data);
      } catch {}
      setAnalysisStage('done');
    } catch (unexpectedErr) {
      setError(unexpectedErr instanceof Error ? unexpectedErr.message : 'Unexpected analysis error.');
      setAnalysisStage('error');
    }
  };`);

const oldControls = `<button
                  onClick={connectionState === 'Disconnected' ? () => activeSession && startLiveDetection(activeSession.session_id) : stopLiveDetection}
                  className={\`px-6 py-2 \${connectionState === 'Disconnected' ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(37,99,235,0.4)]' : 'bg-red-600/20 text-red-500 border border-red-900/50 hover:bg-red-600/30'} text-sm font-semibold rounded-lg transition-all flex items-center\`}
                >
                  {connectionState === 'Disconnected' ? (
                    <><Mic size={16} className="mr-2" /> Start Live Mic</>
                  ) : (
                    <><div className="w-2 h-2 rounded-full bg-red-500 mr-2 animate-pulse" /> Stop</>
                  )}
                </button>
                <button
                  onClick={() => setDetectionMode(detectionMode === 'batch' ? 'Live' : 'batch')}
                  className="px-6 py-2 bg-[#121d30] border border-[#1a2333] hover:bg-[#1a2333] text-gray-300 text-sm font-semibold rounded-lg transition-all flex items-center"
                >
                  Mode: {detectionMode}
                </button>`;

const newControls = `<button
                  onClick={connectionState === 'Disconnected' ? () => { setDetectionMode('Live'); activeSession && startLiveDetection(activeSession.session_id); } : stopLiveDetection}
                  className={\`px-6 py-2 \${connectionState === 'Disconnected' ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(37,99,235,0.4)]' : 'bg-red-600/20 text-red-500 border border-red-900/50 hover:bg-red-600/30'} text-sm font-semibold rounded-lg transition-all flex items-center\`}
                >
                  {connectionState === 'Disconnected' ? (
                    <><Mic size={16} className="mr-2" /> Start Live Mic</>
                  ) : (
                    <><div className="w-2 h-2 rounded-full bg-red-500 mr-2 animate-pulse" /> Stop</>
                  )}
                </button>
                
                <label className="px-6 py-2 bg-[#121d30] border border-[#1a2333] hover:bg-[#1a2333] text-gray-300 text-sm font-semibold rounded-lg transition-all flex items-center cursor-pointer">
                  <FileAudio size={16} className="mr-2" />
                  Upload WAV
                  <input 
                    type="file" 
                    accept="audio/wav" 
                    className="hidden" 
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file && activeSession) {
                        setDetectionMode('batch');
                        if(connectionState !== 'Disconnected') stopLiveDetection();
                        handleRunAnalysis(file);
                      }
                    }} 
                  />
                </label>`;

c = c.replace(oldControls, newControls);

c = c.replace(/\/\* STAGE_LABELS \*\//g, `const STAGE_LABELS: Record<AnalysisStage, string> = {
  idle: '',
  decoding: 'Decoding audio...',
  voice: 'Analyzing voice integrity...',
  speech: 'Transcribing speech...',
  risk: 'Calculating risk score...',
  policy: 'Evaluating policy...',
  done: 'Analysis complete.',
  error: 'Analysis failed.',
};`);

fs.writeFileSync('frontend/src/pages/Dashboard.tsx', c);
