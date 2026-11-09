
    // Nội điện đặt ở không gian riêng (300, 0, 300), layer 1 (đèn riêng, tối hơn)
    temple.position.set(300, 0, 300);
    setLayerRecursive(temple, 1);
    // Đèn nội điện theo grade D2 (layer 1)
    const buddhaSpot = new THREE.SpotLight(0xffdf78, 6.5, 40, Math.PI / 3.5, 0.6);
    buddhaSpot.position.set(300, 10, 300 - 8);
    buddhaSpot.target.position.set(300, 7.5, 300 - 18.7);
    buddhaSpot.layers.set(1);
    temple.add(buddhaSpot); temple.add(buddhaSpot.target);
    const buddhaPoint = new THREE.PointLight(0xffd166, 2.6, 18);
    buddhaPoint.position.set(300, 8.5, 300 - 16.5);
    buddhaPoint.layers.set(1);
    temple.add(buddhaPoint);
    const leftWallLight = new THREE.PointLight(0xffaa00, 1.6, 38);
    leftWallLight.position.set(300 - 10, 6.0, 300);
    leftWallLight.layers.set(1);
    temple.add(leftWallLight);
    const rightWallLight = new THREE.PointLight(0xffaa00, 1.6, 38);
    rightWallLight.position.set(300 + 10, 6.0, 300);
    rightWallLight.layers.set(1);
    temple.add(rightWallLight);
    // Nến bàn thờ: 2 đèn nến riêng (flicker ±15% ~7Hz, G5) — đặt ở phần khói/ánh sáng
    const candleLights = [];
    [-4.8, 4.8].forEach(dx => {
      const cl = new THREE.PointLight(0xffaa00, 1.0, 8);
      cl.position.set(300 + dx, 4.4, 300 + altarZ + 1.5);
      cl.layers.set(1);
      temple.add(cl);
      candleLights.push(cl);
    });

    // ---- Toast (dùng chung cho modal handlers) ----
    let toastTimer;
    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => t.classList.remove('show'), 2800);
    }
    window.showToast = showToast;
