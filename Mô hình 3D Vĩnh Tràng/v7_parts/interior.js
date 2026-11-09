    // 6. BUILD CHÁNH ĐIỆN CHÙA VĨNH TRÀNG 3D CARTOON
    const temple = new THREE.Group();
    scene.add(temple);

    function addBoxT(x, y, z, w, h, d, m, parent=temple) {
      const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
      o.position.set(x, y, z);
      o.castShadow = true; o.receiveShadow = true;
      parent.add(o);
      return o;
    }

    function addCylT(x, y, z, r, h, m, parent=temple, r2=r) {
      const o = new THREE.Mesh(new THREE.CylinderGeometry(r2, r, h, 24), m);
      o.position.set(x, y, z);
      o.castShadow = true; o.receiveShadow = true;
      parent.add(o);
      return o;
    }

    function addBallT(x, y, z, r, m, parent=temple) {
      const o = new THREE.Mesh(new THREE.SphereGeometry(r, 24, 20), m);
      o.position.set(x, y, z);
      o.castShadow = true; o.receiveShadow = true;
      parent.add(o);
      return o;
    }

    // Không gian Chánh Điện (Rộng 28m, Dài 46m, Cao 10m)
    addBoxT(0, 0, 0, 28, 0.2, 46, floorMat);
    addBoxT(0, 5, -23, 28, 10, 0.8, wallMat);
    addBoxT(-14, 5, 0, 0.8, 10, 46, wallMat);
    addBoxT(14, 5, 0, 0.8, 10, 46, wallMat);
    addBoxT(0, 10, 0, 28, 0.4, 46, woodDark);

    // Hàng cột tròn sơn son đỏ tươi bo tròn bóng mịn
    const pillarZ = [-18, -10, -2, 6, 14, 20];
    pillarZ.forEach(pz => {
      [-8.5, 8.5].forEach(px => {
        addCylT(px, 0.35, pz, 1.2, 0.5, mat(0xffb703, 0.3, 0.5));
        addCylT(px, 5.2, pz, 0.48, 9.4, pillarMat);
        addCylT(px, 9.8, pz, 0.9, 0.4, goldMat);
      });
    });

    // Hai Cột Rồng Thếp Vàng Chibi uốn lượn hai bên Tam Bảo
    [-8.5, 8.5].forEach(px => {
      for (let y = 1.8; y <= 8.5; y += 1.4) {
        addCylT(px, y, -10, 0.62, 0.35, goldMat);
      }
      addBoxT(px + (px > 0 ? -0.45 : 0.45), 5.2, -10, 0.12, 6.2, 0.55, goldMat);
    });

    // 3 ĐÈN CHÙM PHA LÊ KIỂU PHÁP CARTOON (Bóng lấp lánh như kẹo ngọc)
    [-10, 0, 10].forEach(cz => {
      const chGroup = new THREE.Group();
      temple.add(chGroup);
      const c1 = addCylT(0, 9.2, cz, 0.04, 1.6, goldMat, chGroup); c1.castShadow = false;
      const c2 = addCylT(0, 8.2, cz, 1.3, 0.15, goldMat, chGroup); c2.castShadow = false;
      const c3 = addCylT(0, 7.8, cz, 0.9, 0.15, goldMat, chGroup); c3.castShadow = false;
      const c4 = addCylT(0, 7.4, cz, 0.5, 0.15, goldMat, chGroup); c4.castShadow = false;

      for (let a = 0; a < Math.PI * 2; a += Math.PI / 4) {
        const cx = Math.cos(a) * 1.15;
        const cy = Math.sin(a) * 1.15;
        const b = addBallT(cx, 8.1, cz + cy, 0.12, mat(0xfff3bf, 0.1, 0, 1, 3.5), chGroup);
        b.castShadow = false;
      }
      const clight = new THREE.PointLight(0xffd166, 1.2, 20); // v4: D2
      clight.position.set(0, 7.6, cz);
      temple.add(clight); // v4: đèn trong điện
    });

    // HOÀNH PHI 「黃金寶殿」 (HOÀNG KIM BỬU ĐIỆN) & 「勅賜 永長寺」
    addBoxT(0, 9.0, -13, 8.8, 1.4, 0.25, goldMat);
    addBoxT(0, 9.0, -12.85, 8.2, 1.0, 0.1, pillarMat);

    // BÀN THỜ TAM BẢO ĐỒ SỘ 3 CẤP
    const altarZ = -16.5;
    addBoxT(0, 1.2, altarZ, 14.0, 2.2, 5.0, mat(0x6b1d16, 0.4));
    addBoxT(0, 2.35, altarZ, 14.2, 0.15, 5.2, goldMat);
    addBoxT(0, 3.0, altarZ - 1.2, 11.0, 1.6, 3.2, mat(0x6b1d16, 0.4));
    addBoxT(0, 3.85, altarZ - 1.2, 11.2, 0.12, 3.4, goldMat);
    addBoxT(0, 4.5, altarZ - 2.2, 8.0, 1.4, 2.4, goldMat);

    // =========================================================================
    // ĐẠI TƯỢNG PHẬT THÍCH CA CHIBI VÀNG 24K TRÊN ĐÀI SEN HOẠT HÌNH
    // =========================================================================
    const bZ = altarZ - 2.2;
    const buddhaGroup = new THREE.Group();
    buddhaGroup.position.set(0, 0, bZ);
    temple.add(buddhaGroup);

    // Tòa sen hoạt hình 3 tầng với 16 cánh sen 3D bo tròn xung quanh
    addCylT(0, 5.4, 0, 2.6, 0.6, goldMat, buddhaGroup);
    addCylT(0, 5.9, 0, 2.2, 0.5, mat(0xffffff), buddhaGroup);

    // 16 cánh hoa sen 3D cánh hồng đầu trắng vươn lên
    for (let i = 0; i < 16; i++) {
      const ang = (i / 16) * Math.PI * 2;
      const px = Math.cos(ang) * 2.1;
      const pz = Math.sin(ang) * 2.1;
      const petal = addBallT(px, 6.2, pz, 0.38, lotusPinkMat, buddhaGroup);
      petal.scale.set(0.8, 1.4, 0.4);
      petal.rotation.y = -ang + Math.PI / 2;
      petal.rotation.z = Math.PI / 8;
    }

    // Chân xếp kiết già (Lotus posture base)
    const legBase = addCylT(0, 6.3, 0, 1.6, 0.5, buddhaMat, buddhaGroup);
    legBase.scale.set(1.4, 1.0, 1.0);

    // Thân Phật Chibi ngồi trang nghiêm
    const bBody = addBallT(0, 7.3, 0, 1.35, buddhaMat, buddhaGroup);
    bBody.scale.set(1.2, 1.25, 0.95);

    // Y cà sa vàng vắt qua vai
    const sash = addBoxT(0.25, 7.4, 0.15, 0.35, 1.4, 0.9, mat(0xf77f00, 0.4), buddhaGroup);

    // Hai cánh tay & Hai bàn tay chắp ấn Thiền Định (Dhyana Mudra)
    const leftArm = addCylT(-1.0, 6.9, 0.1, 0.28, 1.0, buddhaMat, buddhaGroup);
    leftArm.rotation.z = Math.PI / 4;
    const rightArm = addCylT(1.0, 6.9, 0.1, 0.28, 1.0, buddhaMat, buddhaGroup);
    rightArm.rotation.z = -Math.PI / 4;

    // Hai bàn tay Chibi tròn đặt ngửa lên nhau nâng đóa sen vàng
    addBallT(0, 6.45, 0.65, 0.26, buddhaMat, buddhaGroup);
    const jewel = addBallT(0, 6.65, 0.65, 0.18, mat(0xffe066, 0.1, 0, 1, 3.0), buddhaGroup);

    // Đầu Phật Chibi - QUAN TRỌNG: xoay rotation.y = Math.PI để khuôn mặt hướng thẳng ra trước
    const buddhaHead = new THREE.Mesh(
      new THREE.SphereGeometry(0.78, 28, 24),
      new THREE.MeshStandardMaterial({
        map: faceBuddhaTex,
        roughness: 0.2,
        metalness: 0.25
      })
    );
    buddhaHead.position.set(0, 9.05, 0);
    buddhaHead.rotation.y = Math.PI; // Hướng khuôn mặt từ bi ra ngoài về phía Phật tử
    buddhaGroup.add(buddhaHead);

    // Nhục kế tròn Ushnisha trên đỉnh đầu
    addBallT(0, 9.85, 0, 0.32, buddhaMat, buddhaGroup);
    addBallT(0, 10.15, 0, 0.12, mat(0xffffff, 0.1, 0, 1, 4.0), buddhaGroup);

    // Đôi tai Phật dài bo tròn phúc hậu
    const leftEar = addCylT(-0.8, 9.0, 0, 0.1, 0.45, buddhaMat, buddhaGroup);
    const rightEar = addCylT(0.8, 9.0, 0, 0.1, 0.45, buddhaMat, buddhaGroup);

    // ĐẠI HÀO QUANG CẦU VỒNG HOẠT HÌNH
    const haloGroup = new THREE.Group();
    haloGroup.position.set(0, 8.9, -0.4);
    buddhaGroup.add(haloGroup);

    const haloRing1 = addCylT(0, 0, 0, 2.6, 0.05, mat(0xffffff, 0.1, 0, 1, 3.2), haloGroup);
    haloRing1.rotation.x = Math.PI / 2;
    const haloRing2 = addCylT(0, 0, -0.04, 3.3, 0.04, mat(0xffd166, 0.1, 0, 1, 2.6), haloGroup);
    haloRing2.rotation.x = Math.PI / 2;
    const haloRing3 = addCylT(0, 0, -0.08, 4.0, 0.04, mat(0x06d6a0, 0.1, 0, 1, 2.2), haloGroup);
    haloRing3.rotation.x = Math.PI / 2;
    const haloRing4 = addCylT(0, 0, -0.12, 4.8, 0.03, mat(0xef476f, 0.1, 0, 1, 2.0), haloGroup);
    haloRing4.rotation.x = Math.PI / 2;

    // Hai vị thị giả A Nan - Ca Diếp Chibi chắp tay
    [-4.5, 4.5].forEach((ax) => {
      addCylT(ax, 3.8, altarZ - 1.2, 0.8, 0.6, goldMat);
      addCylT(ax, 5.1, altarZ - 1.2, 0.45, 2.0, goldMat);
      const dHead = addBallT(ax, 6.4, altarZ - 1.2, 0.4, new THREE.MeshStandardMaterial({ map: faceMonkTex, roughness: 0.3 }));
      dHead.rotation.y = Math.PI;
    });

    // Bát hương đồng tròn mập & Khói mây hoạt hình
    addCylT(0, 2.8, altarZ + 1.8, 0.65, 0.7, mat(0x8c5e32, 0.35, 0.8));
    for (let h = -0.12; h <= 0.12; h += 0.12) {
      addCylT(h, 3.7, altarZ + 1.8, 0.02, 1.2, mat(0xe63946, 0.6));
      addBallT(h, 4.35, altarZ + 1.8, 0.05, mat(0xffaa00, 0.1, 0, 1, 5.0));
    }

    // Đèn Dược Sư hoa sen phát sáng
    [-4.8, 4.8].forEach(dx => {
      addCylT(dx, 3.2, altarZ + 1.5, 0.25, 1.4, goldMat);
      addBallT(dx, 4.1, altarZ + 1.5, 0.38, lotusPinkMat);
      addBallT(dx, 4.28, altarZ + 1.5, 0.14, mat(0xffaa00, 0.1, 0, 1, 6.0));
    });

    // Cặp Lộc Bình men hoa lam cắm sen hồng
    addCylT(-2.4, 2.8, altarZ + 1.6, 0.25, 0.7, mat(0x48cae4, 0.3, 0.4));
    addBallT(-2.4, 3.4, altarZ + 1.6, 0.38, lotusPinkMat);
    addCylT(2.4, 2.8, altarZ + 1.6, 0.25, 0.7, mat(0x48cae4, 0.3, 0.4));
    addBallT(2.4, 3.4, altarZ + 1.6, 0.38, lotusPinkMat);

    // =========================================================================
