    // 4. CARTOON VIBRANT MATERIALS
    const mat = (c, r=0.45, m=0.0, e=0, ei=0) => new THREE.MeshStandardMaterial({
      color: c, roughness: r, metalness: m,
      emissive: e ? c : 0, emissiveIntensity: Math.min(ei, 2.2) // v4: trần emissive D2
    });

    const floorMat = new THREE.MeshStandardMaterial({
      map: floorTexture,
      roughness: 0.2,
      metalness: 0.15,
    });

    const pillarMat = mat(0xd90429, 0.3, 0.05); // Cột sơn son đỏ tươi bóng
    const wallMat = mat(0xfff3bf, 0.65, 0.0); // Tường vàng kem ấm
    const goldMat = mat(0xffd166, 0.22, 0.88); // Vàng hoàng kim tươi sáng
    const buddhaMat = mat(0xffb703, 0.2, 0.9); // Kim thân Phật dát vàng óng ánh
    const arhatMat = mat(0xffc300, 0.22, 0.88); // 18 La Hán Chibi vàng óng
    const lotusPinkMat = mat(0xff5d8f, 0.4); // Cánh hoa sen hồng tươi
    const lotusWhiteMat = mat(0xffffff, 0.35); // Đầu cánh sen trắng
    const woodDark = mat(0x4a1e13, 0.6); // Gỗ mun ấm
    const matRug = mat(0x9d0208, 0.65); // Thảm đỏ tươi
    const cushionMat = mat(0x7209b7, 0.55); // Bồ đoàn tím sen
    const haloMat = mat(0xffe066, 0.1, 0, 1, 2.2);

    // Materials cho các chú thú cưng Chibi
    const deerMat = mat(0xddb892, 0.45, 0.1);
    const tigerMat = mat(0xf77f00, 0.35, 0.15);
    const dragonMat = mat(0x06d6a0, 0.3, 0.25);
    const elephantMat = mat(0xfdf0d5, 0.35, 0.1);
    const lionMat = mat(0xffb703, 0.4, 0.2);

