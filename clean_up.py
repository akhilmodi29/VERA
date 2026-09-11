with open('frontend/src/pages/Dashboard.tsx', 'r', encoding='utf-8') as f:
    original_content = f.read()

# Get everything up to the eturn (
prefix = original_content.split('  return (')[0]

# Now, we manually clean up the prefix.
# 1. Remove unused icons
prefix = prefix.replace("  Clock,\n", "")
prefix = prefix.replace("  Info,\n", "")
prefix = prefix.replace("  Users,\n", "")

# 2. Add transcript and voice_integrity_score mapping safely
prefix = prefix.replace("contributing_signals: telemetry.signals ?? [],\n        }", "contributing_signals: telemetry.signals ?? [],\n          transcript: telemetry.transcript,\n          voice_integrity_score: telemetry.voice_integrity_score,\n        }")
prefix = prefix.replace("contributing_signals: batchRisk.contributing_signals,\n        }", "contributing_signals: batchRisk.contributing_signals,\n          transcript: batchRisk.transcript,\n          voice_integrity_score: batchRisk.voice_integrity_score,\n        }")

# 3. Clean up the unused derived functions
lines = prefix.split('\n')
new_lines = []
skip = False
for line in lines:
    if line.startswith("  const handleGenerateLiveEvidence = async () => {"):
        skip = True
    elif line.startswith("  const handleEndSession = () => {"):
        skip = True
    elif line.startswith("  const voiceIntegrityDisplay = (() => {"):
        skip = True
    elif line.startswith("  const voiceLabelDisplay = (() => {"):
        skip = True
    elif line.startswith("  const speakerDisplay = (() => {"):
        skip = True
    elif line.startswith("  const transcriptDisplay = (() => {"):
        skip = True
        
    # Also ignore ctiveError since we don't use it in our new JSX
    if line.startswith("  const activeError ="):
        continue

    if skip and line == "  };":
        skip = False
        continue
    elif skip and line == "  })();":
        skip = False
        continue
        
    if not skip:
        new_lines.append(line)

new_prefix = '\n'.join(new_lines)

new_jsx = '''
    <div className="space-y-6 max-w-[1600px] mx-auto pb-12 animate-fade-in">

      {/* Control Strip */}
      <div className="bg-[#0A0D14]/80 backdrop-blur-md border border-vera-border rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 shadow-[0_4px_20px_rgba(0,0,0,0.5)]">
        <div className="flex items-center space-x-6 w-full md:w-auto">
          <div className="flex items-center">
            <div className={elative flex items-center justify-center w-12 h-12 rounded-xl border }>
              {isMicActive ? (
                <>
                  <div className="absolute inset-0 rounded-xl bg-vera-danger/20 animate-ping-slow" />
                  <Mic size={24} className="relative z-10 animate-pulse-fast" />
                </>
              ) : isProcessing ? (
                <Loader2 size={24} className="animate-spin" />
              ) : (
                <ShieldCheck size={24} />
              )}
            </div>
            <div className="ml-4">
              <h2 className="text-sm font-bold text-white tracking-widest uppercase">{activeSession ? 'Session Active' : 'System Standby'}</h2>
              <p className="text-[10px] text-vera-textMuted tracking-wider font-mono">
                {activeSession ? ID:  : 'AWAITING INITIALIZATION'}
              </p>
            </div>
          </div>

          {activeSession && (
            <div className="h-8 w-px bg-vera-border hidden md:block" />
          )}

          {activeSession && (
            <div className="flex bg-[#06080D] p-1 rounded-lg border border-vera-border shadow-inner">
              <button
                onClick={() => setDetectionMode('batch')}
                className={px-4 py-1.5 text-xs font-bold rounded-md uppercase tracking-wider transition-all }
              >
                Batch
              </button>
              <button
                onClick={() => setDetectionMode('live')}
                className={px-4 py-1.5 text-xs font-bold rounded-md uppercase tracking-wider transition-all }
              >
                Live Stream
              </button>
            </div>
          )}
        </div>

        <div className="flex items-center space-x-3 w-full md:w-auto">
          {!activeSession ? (
            <button
              onClick={handleStartSession}
              disabled={isInitializing}
              className="w-full md:w-auto px-8 py-3 bg-vera-accent hover:bg-blue-400 text-white text-xs font-bold uppercase tracking-widest rounded-xl transition-all shadow-[0_0_20px_rgba(59,130,246,0.4)] hover:shadow-[0_0_30px_rgba(59,130,246,0.6)] disabled:opacity-50 flex items-center justify-center"
            >
              {isInitializing ? <Loader2 size={16} className="animate-spin mr-2" /> : <Activity size={16} className="mr-2" />}
              Initialize Session
            </button>
          ) : detectionMode === 'batch' ? (
            <>
              {isRecording ? (
                <button
                  onClick={stopRecording}
                  className="px-6 py-2.5 bg-vera-danger/20 text-vera-danger border border-vera-danger/50 hover:bg-vera-danger/30 text-xs font-bold uppercase tracking-widest rounded-xl transition-all flex items-center"
                >
                  <span className="w-2 h-2 rounded-full bg-vera-danger animate-pulse mr-2" />
                  Stop ({formatTime(recordingTime)})
                </button>
              ) : (
                <button
                  onClick={startRecording}
                  disabled={isProcessing}
                  className="px-6 py-2.5 bg-vera-panel border border-vera-border hover:bg-vera-border text-white text-xs font-bold uppercase tracking-widest rounded-xl transition-all flex items-center disabled:opacity-50"
                >
                  <Mic size={16} className="mr-2" />
                  {audioBlob ? 'Re-record' : 'Record Audio'}
                </button>
              )}
              {audioBlob && !isRecording && (
                <button
                  onClick={handleRunAnalysis}
                  disabled={isProcessing}
                  className="px-8 py-2.5 bg-vera-success/20 text-vera-success border border-vera-success/50 hover:bg-vera-success/30 text-xs font-bold uppercase tracking-widest rounded-xl transition-all flex items-center shadow-[0_0_15px_rgba(16,185,129,0.3)] disabled:opacity-50"
                >
                  {isProcessing ? <Loader2 size={16} className="animate-spin mr-2" /> : <ShieldCheck size={16} className="mr-2" />}
                  Analyze Target
                </button>
              )}
            </>
          ) : (
            <div className="flex items-center space-x-3">
              {connectionState === 'Disconnected' || connectionState === 'disconnected' ? (
                <button
                  onClick={startLiveDetection}
                  disabled={!activeSession}
                  className="px-8 py-2.5 bg-vera-danger/20 text-vera-danger border border-vera-danger/50 hover:bg-vera-danger/30 text-xs font-bold uppercase tracking-widest rounded-xl transition-all flex items-center shadow-[0_0_15px_rgba(239,68,68,0.3)]"
                >
                  <Radio size={16} className="mr-2" /> Engage Stream
                </button>
              ) : (
                <button
                  onClick={stopLiveDetection}
                  className="px-8 py-2.5 bg-vera-panel border border-vera-border hover:bg-vera-border text-white text-xs font-bold uppercase tracking-widest rounded-xl transition-all flex items-center"
                >
                  Disconnect Stream
                </button>
              )}
              <div className="flex items-center px-4 py-2.5 bg-[#06080D] border border-vera-border rounded-xl">
                <span className={w-2 h-2 rounded-full mr-2 } />
                <span className="text-[10px] font-mono text-vera-textMuted uppercase">{connectionState}</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {(error || liveError || recorderError || decisionError) && (
        <div className="p-4 bg-vera-danger/10 border border-vera-danger/30 rounded-xl flex items-start text-vera-danger animate-fade-in shadow-[0_0_15px_rgba(239,68,68,0.1)]">
          <AlertTriangle size={18} className="mr-3 mt-0.5 shrink-0" />
          <div className="text-sm font-medium tracking-wide">
            {error || liveError || recorderError || decisionError}
          </div>
        </div>
      )}

      {/* Main Intelligence Grid */}
      {!activeSession ? (
        <div className="flex flex-col items-center justify-center py-32 px-4 border border-vera-border/50 border-dashed rounded-3xl bg-gradient-to-b from-transparent to-[#0A0D14]/50">
          <div className="relative mb-8">
            <div className="absolute inset-0 bg-vera-accent/20 blur-[50px] rounded-full" />
            <ShieldCheck size={80} className="text-vera-border relative z-10 stroke-[1]" />
          </div>
          <h2 className="text-xl font-bold text-white tracking-widest uppercase mb-2">VERA Command Center</h2>
          <p className="text-vera-textMuted text-sm max-w-md text-center tracking-wide leading-relaxed">
            Awaiting session initialization. The acoustic threat intelligence module is currently in standby mode.
          </p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* Left Col: Transcript & Timeline (7 cols) */}
            <div className="lg:col-span-7 space-y-6">
              
              {/* Live Transcript Console */}
              <div className="bg-[#0A0D14]/80 backdrop-blur-sm border border-vera-border rounded-2xl shadow-xl overflow-hidden flex flex-col h-[400px]">
                <div className="bg-[#06080D] px-5 py-3 border-b border-vera-border flex items-center justify-between">
                  <div className="flex items-center text-xs font-bold text-white uppercase tracking-widest">
                    <MessageSquareWarning size={14} className="mr-2 text-vera-accent" /> Signal Intercept
                  </div>
                  {isProcessing && <div className="text-[10px] font-mono text-vera-accent animate-pulse">DECRYPTING AUDIO...</div>}
                </div>
                <div className="flex-1 p-5 overflow-y-auto font-mono text-sm leading-relaxed text-gray-300 relative">
                  {detectionMode === 'batch' ? (
                    displayRiskData?.transcript ? (
                      <div className="animate-fade-in">
                        <span className="text-vera-accent mr-2">&gt;</span>
                        {displayRiskData.transcript}
                      </div>
                    ) : (
                      <div className="flex items-center justify-center h-full text-vera-textMuted/50 text-xs italic">
                        No transmission intercepted
                      </div>
                    )
                  ) : (
                    <div className="space-y-3">
                      {telemetryHistory.length > 0 ? (
                        [...telemetryHistory].map((evt, idx) => (
                          <div key={idx} className="animate-fade-in border-l-2 border-vera-border pl-3 ml-1">
                            <div className="text-[10px] text-vera-textMuted mb-1">{evt.timestamp ? new Date(evt.timestamp).toLocaleTimeString() : 'SYS'}</div>
                            <div><span className="text-vera-accent mr-2">&gt;</span>{evt.transcript || '<silence>'}</div>
                          </div>
                        ))
                      ) : (
                        <div className="flex items-center justify-center h-full text-vera-textMuted/50 text-xs italic">
                          Awaiting stream packets...
                        </div>
                      )}
                    </div>
                  )}
                  {isProcessing && (
                    <div className="absolute bottom-4 left-5 flex items-center text-[10px] text-vera-accent tracking-widest uppercase bg-[#0A0D14]/90 px-3 py-1.5 rounded-full border border-vera-accent/20">
                      <div className="w-1.5 h-1.5 bg-vera-accent rounded-full animate-ping mr-2" /> {analysisStage !== 'idle' ? STAGE_LABELS[analysisStage as AnalysisStage] : 'Receiving...'}
                    </div>
                  )}
                </div>
              </div>

              {/* Threat Signals Bar */}
              <div className="bg-[#0A0D14]/80 backdrop-blur-sm border border-vera-border rounded-2xl p-5 shadow-xl min-h-[120px]">
                <div className="text-xs font-bold text-white uppercase tracking-widest mb-4 flex items-center">
                  <Fingerprint size={14} className="mr-2 text-vera-warning" /> Detected Threat Vectors
                </div>
                <div className="flex flex-wrap gap-2">
                  {displayRiskData?.contributing_signals && displayRiskData.contributing_signals.length > 0 ? (
                    displayRiskData.contributing_signals.map((sig, i) => (
                      <span
                        key={i}
                        className="px-3 py-1.5 bg-vera-warning/10 border border-vera-warning/30 rounded text-[10px] font-bold text-vera-warning uppercase tracking-wider animate-fade-in shadow-[0_0_10px_rgba(245,158,11,0.1)]"
                      >
                        [{sig.replace(/_/g, ' ')}]
                      </span>
                    ))
                  ) : (
                    <span className="text-[10px] font-mono text-vera-textMuted uppercase tracking-widest">
                      {isProcessing ? 'Scanning vectors...' : 'No anomalous vectors detected'}
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Right Col: Risk & Decision Metrics (5 cols) */}
            <div className="lg:col-span-5 space-y-6 flex flex-col">
              
              {/* Primary Risk Metric */}
              <div className={elative overflow-hidden border rounded-2xl p-6 shadow-2xl transition-all duration-500 }>
                {displayRiskData?.risk_level === 'critical' && (
                  <div className="absolute inset-0 bg-red-500/5 animate-pulse-fast pointer-events-none" />
                )}
                
                <div className="flex justify-between items-start mb-6 relative z-10">
                  <div className="text-xs font-bold text-white uppercase tracking-widest flex items-center">
                    <AlertOctagon size={14} className="mr-2" /> Threat Level
                  </div>
                  {displayRiskData?.risk_level && (
                    <div className={px-3 py-1 rounded text-[10px] font-black uppercase tracking-widest }>
                      {displayRiskData.risk_level}
                    </div>
                  )}
                </div>

                <div className="flex items-end space-x-2 relative z-10">
                  <span className={	ext-6xl font-light tracking-tighter }>
                    {displayRiskData?.overall_risk_score !== undefined ? (displayRiskData.overall_risk_score * 100).toFixed(0) : '--'}
                  </span>
                  <span className="text-sm text-vera-textMuted font-bold mb-2">%</span>
                </div>
                
                {/* Visual Risk Bar */}
                <div className="mt-6 h-1.5 w-full bg-[#06080D] rounded-full overflow-hidden relative z-10">
                  <div 
                    className={h-full transition-all duration-1000 ease-out }
                    style={{ width: ${displayRiskData?.overall_risk_score ? displayRiskData.overall_risk_score * 100 : 0}% }}
                  />
                </div>
              </div>

              {/* Sub Metrics Grid */}
              <div className="grid grid-cols-2 gap-4 flex-1">
                {/* Voice Integrity */}
                <div className="bg-[#0A0D14]/80 backdrop-blur-sm border border-vera-border rounded-2xl p-5 shadow-xl flex flex-col justify-between">
                  <div className="text-[10px] font-bold text-vera-textMuted uppercase tracking-widest flex items-center mb-3">
                    <FileAudio size={12} className="mr-1.5" /> Acoustic Integrity
                  </div>
                  <div>
                    <div className="text-2xl font-light text-white">
                      {displayRiskData?.voice_integrity_score !== undefined 
                        ? ${(displayRiskData.voice_integrity_score * 100).toFixed(1)}% 
                        : '--'}
                    </div>
                    <div className="text-[10px] uppercase font-mono tracking-wider mt-1 text-gray-500">
                      Synthesis Prob
                    </div>
                  </div>
                </div>

                {/* Policy Decision */}
                <div className="bg-[#0A0D14]/80 backdrop-blur-sm border border-vera-border rounded-2xl p-5 shadow-xl flex flex-col justify-between relative overflow-hidden">
                  <div className="text-[10px] font-bold text-vera-textMuted uppercase tracking-widest flex items-center mb-3 relative z-10">
                    <ShieldAlert size={12} className="mr-1.5" /> Policy Enforcer
                  </div>
                  <div className="relative z-10">
                    <div className={	ext-xl font-bold uppercase tracking-widest }>
                      {displayDecisionData?.decision || 'STANDBY'}
                    </div>
                    <div className="text-[10px] uppercase font-mono tracking-wider mt-1 text-gray-500 truncate">
                      {displayDecisionData?.decision === 'allow' ? 'Transact Auth' : 
                       displayDecisionData?.decision === 'block' ? 'Conn Terminated' : 'Awaiting Data'}
                    </div>
                  </div>
                  {/* Subtle background icon */}
                  <ShieldCheck size={80} className="absolute -bottom-4 -right-4 text-white/[0.02] pointer-events-none" />
                </div>
              </div>
            </div>
          </div>

          {/* Cryptographic Ledger */}
          <div className="bg-[#0A0D14]/90 backdrop-blur-md border border-vera-border rounded-2xl p-6 shadow-xl mt-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xs font-bold text-white uppercase tracking-widest flex items-center">
                <FileText className="mr-2 text-vera-accent" size={14} /> Cryptographic Evidence Ledger
              </h3>
              {evidenceData && (
                <div className="text-[10px] font-mono bg-vera-success/10 text-vera-success px-2 py-1 rounded border border-vera-success/20 flex items-center">
                  <CheckCircle2 size={10} className="mr-1" /> VERIFIED
                </div>
              )}
            </div>
            
            <div className="bg-[#06080D] border border-vera-border rounded-xl p-4 font-mono text-xs overflow-hidden h-40 flex flex-col">
              {evidenceData?.evidence_record ? (
                <>
                  <div className="flex items-center space-x-4 mb-3 pb-3 border-b border-vera-border/50">
                    <span className="text-vera-textMuted uppercase tracking-widest text-[9px] shrink-0">SHA-256</span>
                    <span className="text-vera-accent font-bold truncate tracking-wider">{evidenceData.hash}</span>
                  </div>
                  <div className="flex-1 overflow-y-auto custom-scrollbar">
                    <pre className="text-gray-400 text-[10px] leading-relaxed">{JSON.stringify(evidenceData.evidence_record, null, 2)}</pre>
                  </div>
                </>
              ) : (
                <div className="flex-1 flex items-center justify-center text-vera-textMuted/40 italic uppercase tracking-widest text-[10px]">
                  {isProcessing ? 'Computing hash sequence...' : 'Ledger empty'}
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
'''

with open('frontend/src/pages/Dashboard.tsx', 'w', encoding='utf-8') as f:
    f.write(new_prefix + '  return (\n' + new_jsx)

