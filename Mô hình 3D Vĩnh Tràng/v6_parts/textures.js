    // 3. PROCEDURAL CARTOON TEXTURES
    // Mặt Chibi cười tươi má hồng
    function createChibiFaceTexture(type = 'happy') {
      const cv = document.createElement('canvas');
      cv.width = 512;
      cv.height = 512;
      const ctx = cv.getContext('2d');

      // Nền da hồng đào mềm mại
      ctx.fillStyle = '#ffdfba';
      ctx.fillRect(0, 0, 512, 512);

      if (type === 'happy' || type === 'user') {
        // Đôi mắt cười hình trăng lưỡi liềm cong dễ thương
        ctx.strokeStyle = '#381607';
        ctx.lineWidth = 18;
        ctx.lineCap = 'round';

        ctx.beginPath();
        ctx.arc(160, 230, 52, Math.PI * 1.15, Math.PI * 1.85, false);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(352, 230, 52, Math.PI * 1.15, Math.PI * 1.85, false);
        ctx.stroke();

        // Má hồng đào phúng phính (Blush)
        ctx.fillStyle = 'rgba(255, 99, 132, 0.6)';
        ctx.beginPath();
        ctx.arc(120, 285, 45, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(392, 285, 45, 0, Math.PI * 2);
        ctx.fill();

        // Nụ cười hoan hỷ
        ctx.beginPath();
        ctx.arc(256, 290, 32, 0.2, Math.PI - 0.2, false);
        ctx.stroke();

        // Chấm đỏ bindi giữa trán
        ctx.fillStyle = '#d62828';
        ctx.beginPath();
        ctx.arc(256, 140, 14, 0, Math.PI * 2);
        ctx.fill();
      } else if (type === 'buddha') {
        // Mặt Đức Phật Chibi từ bi
        ctx.fillStyle = '#ffe699';
        ctx.fillRect(0, 0, 512, 512);

        ctx.strokeStyle = '#5c3300';
        ctx.lineWidth = 14;
        ctx.lineCap = 'round';

        // Đôi mắt khép hờ tĩnh lặng
        ctx.beginPath();
        ctx.arc(165, 235, 55, Math.PI * 0.1, Math.PI * 0.9, false);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(347, 235, 55, Math.PI * 0.1, Math.PI * 0.9, false);
        ctx.stroke();

        // Nụ cười từ bi
        ctx.beginPath();
        ctx.arc(256, 305, 36, 0.2, Math.PI - 0.2, false);
        ctx.stroke();

        // Bạch hào ngọc trắng
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(256, 150, 18, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffb703';
        ctx.lineWidth = 6;
        ctx.stroke();
      }

      const tex = new THREE.CanvasTexture(cv);
      return tex;
    }

    const faceUserTex = createChibiFaceTexture('user');
    const faceMonkTex = createChibiFaceTexture('happy');
    const faceBuddhaTex = createChibiFaceTexture('buddha');

    // Sàn gạch đỏ men nung Cartoon bóng bẩy
    function createCartoonFloorTexture() {
      const cv = document.createElement('canvas');
      cv.width = 512;
      cv.height = 512;
      const ctx = cv.getContext('2d');
      const size = 128;
      for (let y = 0; y < 4; y++) {
        for (let x = 0; x < 4; x++) {
          const px = x * size;
          const py = y * size;
          ctx.fillStyle = '#3a1106';
          ctx.fillRect(px, py, size, size);

          ctx.fillStyle = '#b8381d';
          ctx.beginPath();
          ctx.roundRect(px + 4, py + 4, size - 8, size - 8, 14);
          ctx.fill();

          const grad = ctx.createRadialGradient(px + size/2, py + size/2, 5, px + size/2, py + size/2, size/2);
          grad.addColorStop(0, '#f2542d');
          grad.addColorStop(0.7, '#cc3b1b');
          grad.addColorStop(1, '#94260f');
          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.roundRect(px + 8, py + 8, size - 16, size - 16, 10);
          ctx.fill();

          ctx.strokeStyle = 'rgba(255, 209, 102, 0.55)';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(px + 10, py + 10, size - 20, size - 20, 8);
          ctx.stroke();
        }
      }
      const tex = new THREE.CanvasTexture(cv);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(16, 26);
      return tex;
    }

    const floorTexture = createCartoonFloorTexture();

