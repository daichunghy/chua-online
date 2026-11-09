    // 1. AUDIO SYNTHESIZER
    let audioCtx = null;
    let isAudioOn = true;

    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
    }

    function playBell() {
      if (!isAudioOn) return;
      initAudio();
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); // D5
      osc.frequency.exponentialRampToValueAtTime(293.66, audioCtx.currentTime + 3.5);
      gain.gain.setValueAtTime(0.55, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 3.8);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 3.8);
    }

    function playMokugyo() {
      if (!isAudioOn) return;
      initAudio();
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(340, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(140, audioCtx.currentTime + 0.12);
      gain.gain.setValueAtTime(0.85, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.14);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.15);
    }

    document.getElementById('btn-audio-toggle').onclick = () => {
      isAudioOn = !isAudioOn;
      document.getElementById('btn-audio-toggle').textContent = isAudioOn ? '🔔 Chuông Mõ: Bật' : '🔕 Chuông Mõ: Tắt';
      if (isAudioOn) playBell();
    };

