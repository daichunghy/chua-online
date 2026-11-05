/**
 * Gemini Live API Avatar Service for Chùa Online
 * 
 * Kết nối thời gian thực hai chiều giữa Avatar 3D (Three.js) và mô hình Gemini Live API (gemini-3.8-live)
 * qua WebSocket / Web Audio API.
 * 
 * Quy chuẩn theo SDK mới nhất @google/genai (v2.3.0+):
 * - Model: gemini-3.8-live (low latency voice agent)
 * - Input: Audio PCM 16-bit little-endian mono 16kHz (audio/pcm;rate=16000)
 * - Output: Audio PCM 16-bit little-endian mono 24kHz
 * - Đồng bộ khẩu hình (Visemes/Lip-sync) & Cử chỉ Phật giáo tương tác
 */

import { GoogleGenAI } from '@google/genai';

export class GeminiLiveAvatarService {
  constructor(options = {}) {
    this.apiKey = options.apiKey || null;
    this.model = options.model || 'gemini-3.8-live';
    this.systemInstruction = options.systemInstruction || 
      'Bạn là một vị tu sĩ Phật giáo hiền hòa, am tường kinh điển tại Chùa Online. ' +
      'Bạn nói năng từ ái, chậm rãi, khoan thai, ngắn gọn, dễ hiểu, ' +
      'hướng dẫn người dùng học Phật, giữ chánh niệm và chuyển hóa phiền não theo tinh thần Chánh kiến và Nhân quả.';
    
    this.session = null;
    this.audioContext = null;
    this.micStream = null;
    this.processor = null;
    this.audioQueue = [];
    this.isPlaying = false;
    this.onVolumeChange = options.onVolumeChange || null; // Callback cập nhật khẩu hình miệng 3D
    this.onTranscription = options.onTranscription || null; // Callback phụ đề văn bản
    this.onInterrupted = options.onInterrupted || null; // Callback khi người dùng ngắt lời
  }

  /**
   * Khởi tạo phiên kết nối Live API qua WebSocket
   */
  async startSession() {
    if (!this.apiKey) {
      throw new Error('Cần cung cấp API Key hoặc Ephemeral Token của Gemini.');
    }

    const ai = new GoogleGenAI({ apiKey: this.apiKey });

    // Cấu hình phiên Live theo chuẩn Gemini 3.8
    this.session = await ai.live.connect({
      model: this.model,
      config: {
        responseModalities: ['audio'],
        systemInstruction: {
          parts: [{ text: this.systemInstruction }]
        },
        inputAudioTranscription: {
          mode: 'smart' // Làm sạch từ đệm, chuẩn hóa tiếng Việt
        },
        outputAudioTranscription: {}
      },
      callbacks: {
        onopen: () => {
          console.log('[GeminiLive] Đã kết nối phiên đàm thoại thời gian thực.');
          this.initMicrophoneCapture();
        },
        onmessage: (response) => {
          this.handleServerEvent(response);
        },
        onerror: (err) => {
          console.error('[GeminiLive] Lỗi kết nối:', err);
        },
        onclose: () => {
          console.log('[GeminiLive] Đã đóng phiên kết nối.');
          this.stopMicrophoneCapture();
        }
      }
    });
  }

  /**
   * Thu âm Micro và chuyển đổi sang PCM 16kHz Little-Endian
   */
  async initMicrophoneCapture() {
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
    this.micStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        channelCount: 1,
        sampleRate: 16000,
        echoCancellation: true,
        noiseSuppression: true
      }
    });

    const source = this.audioContext.createMediaStreamSource(this.micStream);
    
    // ScriptProcessor hoặc AudioWorklet thu thập chunk PCM
    this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);
    this.processor.onaudioprocess = (e) => {
      if (!this.session) return;
      const inputData = e.inputBuffer.getChannelData(0);
      
      // Chuyển Float32 (-1.0 -> 1.0) sang 16-bit PCM little-endian
      const pcm16 = new Int16Array(inputData.length);
      for (let i = 0; i < inputData.length; i++) {
        const s = Math.max(-1, Math.min(1, inputData[i]));
        pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
      }

      // Encode base64
      const base64Audio = this.arrayBufferToBase64(pcm16.buffer);

      // Gửi realtime input lên Gemini Live API
      this.session.sendRealtimeInput({
        audio: {
          data: base64Audio,
          mimeType: 'audio/pcm;rate=16000'
        }
      });
    };

    source.connect(this.processor);
    this.processor.connect(this.audioContext.destination);
  }

  /**
   * Xử lý sự kiện trả về từ Server Gemini
   */
  handleServerEvent(response) {
    const content = response.serverContent;
    if (!content) return;

    // 1. Nhận tín hiệu ngắt lời (Interruption) -> dừng phát âm thanh ngay lập tức
    if (content.interrupted) {
      console.log('[GeminiLive] Người dùng ngắt lời -> Hủy hàng đợi âm thanh.');
      this.audioQueue = [];
      if (this.onInterrupted) this.onInterrupted();
      return;
    }

    // 2. Nhận Audio phản hồi từ Model
    if (content.modelTurn?.parts) {
      for (const part of content.modelTurn.parts) {
        if (part.inlineData && part.inlineData.data) {
          const rawPcm24k = this.base64ToArrayBuffer(part.inlineData.data);
          this.enqueueAudioChunk(rawPcm24k);
        }
      }
    }

    // 3. Nhận bản phiên âm văn bản
    if (content.inputTranscription && this.onTranscription) {
      this.onTranscription({ role: 'user', text: content.inputTranscription.text });
    }
    if (content.outputTranscription && this.onTranscription) {
      this.onTranscription({ role: 'gemini', text: content.outputTranscription.text });
    }
  }

  /**
   * Đưa chunk âm thanh vào hàng đợi phát (PCM 24kHz)
   */
  enqueueAudioChunk(arrayBuffer) {
    this.audioQueue.push(arrayBuffer);
    if (!this.isPlaying) {
      this.playNextChunk();
    }
  }

  async playNextChunk() {
    if (this.audioQueue.length === 0) {
      this.isPlaying = false;
      if (this.onVolumeChange) this.onVolumeChange(0);
      return;
    }

    this.isPlaying = true;
    const chunk = this.audioQueue.shift();

    // Decode PCM 24kHz sang AudioBuffer
    const pcm16 = new Int16Array(chunk);
    const float32 = new Float32Array(pcm16.length);
    let sumSquares = 0;
    for (let i = 0; i < pcm16.length; i++) {
      float32[i] = pcm16[i] / 32768.0;
      sumSquares += float32[i] * float32[i];
    }

    // Tính biên độ RMS để điều khiển khẩu hình nhân vật (Lip-sync)
    const rms = Math.sqrt(sumSquares / pcm16.length);
    if (this.onVolumeChange) {
      this.onVolumeChange(Math.min(rms * 4.0, 1.0));
    }

    if (!this.playbackContext) {
      this.playbackContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 24000 });
    }

    const audioBuf = this.playbackContext.createBuffer(1, float32.length, 24000);
    audioBuf.getChannelData(0).set(float32);

    const source = this.playbackContext.createBufferSource();
    source.buffer = audioBuf;
    source.connect(this.playbackContext.destination);
    source.onended = () => {
      this.playNextChunk();
    };
    source.start();
  }

  /**
   * Ngắt kết nối và giải phóng tài nguyên
   */
  stopSession() {
    this.stopMicrophoneCapture();
    if (this.playbackContext) {
      this.playbackContext.close();
      this.playbackContext = null;
    }
    this.session = null;
  }

  stopMicrophoneCapture() {
    if (this.processor) {
      this.processor.disconnect();
      this.processor = null;
    }
    if (this.micStream) {
      this.micStream.getTracks().forEach(t => t.stop());
      this.micStream = null;
    }
    if (this.audioContext) {
      this.audioContext.close();
      this.audioContext = null;
    }
  }

  arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
  }

  base64ToArrayBuffer(base64) {
    const binary = window.atob(base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
    return bytes.buffer;
  }
}
