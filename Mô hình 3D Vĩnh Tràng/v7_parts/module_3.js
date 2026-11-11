    // ---- 4. NỘI ĐIỆN (giữ nguyên bản dựng v3, đặt ở không gian riêng, layer 1) ----
    // Đi qua cửa + fade 0,4s để vào; nội điện tối hơn một bậc nhờ đèn riêng layer 1.

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

    // 7. BỘ TƯỢNG 18 VỊ LA HÁN CHIBI CƯỠI LINH THÚ HOẠT HÌNH
    // =========================================================================
    const interactiveObjects = [];

    const arhatsLeft = [
      { id: 1, name: "Tọa Lộc La Hán (Tân Đầu Lô Tôn Giả)", mount: "Cưỡi Hươu Sao Chibi", beastType: "deer", desc: "Ngài Tân-đầu-lô cưỡi chú hươu sao mắt tròn đốm trắng, mang năng lượng an nhiên, trường thọ và thanh khiết." },
      { id: 2, name: "Hoan Hỷ La Hán (Ca Nặc Ca Phạt Tha)", mount: "Tọa Sen Vàng", beastType: "lotus", desc: "Tôn giả mang nụ cười Chibi rạng rỡ, đem niềm vui hoan hỷ và tiếng cười an lạc đến cho mọi nhà." },
      { id: 3, name: "Cử Bát La Hán (Ca Nặc Ca Bạt Ly Đọa)", mount: "Nâng Bát Vàng", beastType: "bowl", desc: "Giơ cao bình bát khất thực giáo hóa chúng sinh, trừ bỏ tham xan, huân tu lòng hào phóng bố thí." },
      { id: 4, name: "Thác Tháp La Hán (Tô Tần Đà Tôn Giả)", mount: "Cầm Bảo Tháp", beastType: "pagoda", desc: "Nâng ngọn bảo tháp xá lợi Phật xoay phát sáng, bảo vệ gia quyến khỏi mọi điều xui xẻo u ám." },
      { id: 5, name: "Tĩnh Tọa La Hán (Nặc Cự La Tôn Giả)", mount: "Tọa Phiến Thạch", beastType: "rock", desc: "Thiền định bất động như núi cao, giúp lòng người lắng đọng bớt âu lo, tinh tấn vượt qua khó khăn." },
      { id: 6, name: "Quá Giang La Hán (Bạt Đà La Tôn Giả)", mount: "Cưỡi Cá Kình Con", beastType: "fish", desc: "Cưỡi chú cá kình vượt biển sinh tử, mang lời chúc công việc thuận buồm xuôi gió, tai qua nạn khỏi." },
      { id: 7, name: "Kỵ Tượng La Hán (Ca Lý Ca Tôn Giả)", mount: "Cưỡi Voi Trắng Chibi", beastType: "elephant", desc: "Ngự trên lưng chú voi con trắng ngọc vòi uốn cong giơ hoa sen, biểu thị cho đại phúc đại đức." },
      { id: 8, name: "Tiếu Sư La Hán (Phạt Xà La Phất Đa)", mount: "Cưỡi Sư Tử Bông", beastType: "lion", desc: "Cưỡi chú sư tử bông bờm vàng xù lông ngộ nghĩnh, trừ ma chướng và đem lại dũng khí kiên cường." },
      { id: 9, name: "Khai Tâm La Hán (Tuất Bác Ca Tôn Giả)", mount: "Vạch Ngực Thấy Phật", beastType: "heart", desc: "Mở vạt áo hiện trái tim hoa sen rực sáng, nhắn nhủ Phật tính luôn ngự trong tâm mỗi con người." }
    ];

    const arhatsRight = [
      { id: 10, name: "Thám Thủ La Hán (Bán Thác Ca Tôn Giả)", mount: "Vươn Tay Thư Thái", beastType: "relax", desc: "Vươn hai tay đón lấy ánh bình minh giác ngộ, tâm trí hanh thông, học hành thi cử đỗ đạt." },
      { id: 11, name: "Trầm Tư La Hán (La Hầu La Tôn Giả)", mount: "Tọa Đài Trầm Mặc", beastType: "think", desc: "Con của Đức Phật Thích Ca, mật hạnh đệ nhất, nêu gương hiếu thảo và kiên trì không lùi bước." },
      { id: 12, name: "Trầm Tĩnh La Hán (Na Già Tư Na Tôn Giả)", mount: "Thủ Ấn Tĩnh Tâm", beastType: "calm", desc: "Tâm hồn trong sáng như trăng rằm, hóa giải mọi bất hòa thị phi, gia đạo hòa thuận ấm êm." },
      { id: 13, name: "Phục Hổ La Hán (Phục Hổ Tôn Giả)", mount: "Cưỡi Bạch Hổ Tròn Xoe", beastType: "tiger", desc: "Cưỡi chú cọp béo tròn sọc vằn ngộ nghĩnh bằng lòng từ bi vô lượng, chế ngự nóng giận, đón tài lộc." },
      { id: 14, name: "Hàng Long La Hán (Hàng Long Tôn Giả)", mount: "Cưỡi Kim Long Chibi", beastType: "dragon", desc: "Cưỡi chú rồng vàng nhỏ nhắn mắt to uốn lượn, bảo vệ kinh điển, chiêu tài tiến bảo, may mắn hanh thông." },
      { id: 15, name: "Bố Đại La Hán (Nhân Yết Đà Tôn Giả)", mount: "Mang Túi Vải Thần", beastType: "bag", desc: "Bụng tròn xoe cười toe toét, túi vải may mắn ban phát niềm vui, tiền tài và sức khỏe dồi dào." },
      { id: 16, name: "Ba Tiêu La Hán (Phạt Na Bà Tư Tôn Giả)", mount: "Tọa Lá Ba Tiêu", beastType: "banana", desc: "Ngồi trên tàu lá chuối xanh mát thanh thản, tâm không vướng bận ưu phiền, đời sống an nhiên." },
      { id: 17, name: "Trường Mi La Hán (A Thị Đa Tôn Giả)", mount: "Lông Mày Mây Trắng", beastType: "eyebrow", desc: "Lông mày rủ dài như mây bông bồng bềnh, ban lời chúc thọ khang ninh cho ông bà, cha mẹ." },
      { id: 18, name: "Khán Môn La Hán (Chú Đồ Bán Thác Ca)", mount: "Cầm Tích Trượng", beastType: "staff", desc: "Tay rung trượng đồng có vòng chuông kêu leng keng vui tai, giữ gìn mái ấm bình yên, an vui." }
    ];

    addBoxT(-13.0, 0.7, 0, 1.8, 1.4, 34, mat(0x7f1d1d, 0.4));
    addBoxT(-13.0, 1.45, 0, 1.9, 0.12, 34.2, goldMat);

    addBoxT(13.0, 0.7, 0, 1.8, 1.4, 34, mat(0x7f1d1d, 0.4));
    addBoxT(13.0, 1.45, 0, 1.9, 0.12, 34.2, goldMat);

    function createCartoonArhat(x, z, data, isLeft) {
      const g = new THREE.Group();
      g.position.set(x, 1.5, z);
      g.rotation.y = isLeft ? Math.PI / 2 : -Math.PI / 2;
      temple.add(g);

      // Bệ sen vàng
      addCylT(0, 0.15, 0, 0.7, 0.25, goldMat, g);

      // Thú cưng Chibi
      let bMat = goldMat;
      if (data.beastType === 'tiger') bMat = tigerMat;
      else if (data.beastType === 'dragon') bMat = dragonMat;
      else if (data.beastType === 'elephant') bMat = elephantMat;
      else if (data.beastType === 'deer') bMat = deerMat;
      else if (data.beastType === 'lion') bMat = lionMat;

      const beast = addBallT(0, 0.52, 0, 0.42, bMat, g);
      beast.scale.set(1.25, 0.95, 0.95);
      const beastHead = addBallT(0.42, 0.7, 0, 0.3, bMat, g);

      if (data.beastType === 'elephant') {
        const trunk = addCylT(0.62, 0.8, 0, 0.09, 0.4, elephantMat, g);
        trunk.rotation.z = Math.PI / 4;
        addCylT(0.55, 0.65, 0.14, 0.03, 0.25, mat(0xffffff), g);
        addCylT(0.55, 0.65, -0.14, 0.03, 0.25, mat(0xffffff), g);
        // Tai voi to tròn
        const earL = addBallT(0.35, 0.85, 0.3, 0.22, elephantMat, g); earL.scale.set(0.2, 1, 1);
        const earR = addBallT(0.35, 0.85, -0.3, 0.22, elephantMat, g); earR.scale.set(0.2, 1, 1);
      } else if (data.beastType === 'deer') {
        addCylT(0.42, 1.05, 0.12, 0.02, 0.3, goldMat, g);
        addCylT(0.42, 1.05, -0.12, 0.02, 0.3, goldMat, g);
      } else if (data.beastType === 'lion') {
        addBallT(0.4, 0.7, 0, 0.4, mat(0xfb8500, 0.5), g);
      }

      // Thân La Hán Chibi
      addBallT(0, 1.15, 0, 0.42, arhatMat, g);

      // Đầu Chibi có mặt má hồng mắt cười
      const aHead = new THREE.Mesh(
        new THREE.SphereGeometry(0.34, 20, 18),
        new THREE.MeshStandardMaterial({ map: faceMonkTex, roughness: 0.3 })
      );
      aHead.position.set(0, 1.7, 0);
      aHead.rotation.y = Math.PI; // Hướng mặt ra
      g.add(aHead);

      // Hào quang thiên thần Chibi
      const haloTorus = new THREE.Mesh(
        new THREE.TorusGeometry(0.3, 0.045, 16, 24),
        mat(0xffe066, 0.1, 0, 1, 2.2)
      );
      haloTorus.position.set(0, 1.7, -0.12);
      g.add(haloTorus);

      // Đèn hoa sen phát sáng
      addBallT(0, 0.35, 0.55, 0.14, lotusPinkMat, g);
      addBallT(0, 0.48, 0.55, 0.06, mat(0xffaa00, 0.1, 0, 1, 5.5), g);

      const pt = new THREE.PointLight(0xffb703, 1.4, 6);
      pt.position.set(0, 0.9, 0.55);
      g.add(pt);

      g.userData = {
        isArhat: true,
        data: data,
        worldPos: new THREE.Vector3(x, 2.5, z),
        halo: haloTorus,
        beast: beastHead
      };
      interactiveObjects.push(g);
      return g;
    }

    arhatsLeft.forEach((arh, idx) => {
      const zPos = -15.0 + idx * 3.4;
      createCartoonArhat(-12.8, zPos, arh, true);
    });

    arhatsRight.forEach((arh, idx) => {
      const zPos = -15.0 + idx * 3.4;
      createCartoonArhat(12.8, zPos, arh, false);
    });

    // HAI ĐẠI KHÁM THỜ BỒ TÁT Ở GIỮA HAI VÁCH (Z = 0)
    // 1. Quán Thế Âm Chuẩn Đề Chibi (Vách Tả)
    const qaGroup = new THREE.Group();
    qaGroup.position.set(-13.1, 0, 0);
    qaGroup.rotation.y = Math.PI / 2;
    temple.add(qaGroup);

    addBoxT(0, 3.2, -0.4, 3.2, 6.4, 0.6, goldMat, qaGroup);
    addBoxT(0, 3.2, -0.2, 2.8, 5.8, 0.4, mat(0x9d0208), qaGroup);
    addCylT(0, 1.8, 0, 1.2, 0.6, lotusPinkMat, qaGroup);
    addBallT(0, 2.8, 0, 0.7, buddhaMat, qaGroup);
    const qaHead = new THREE.Mesh(
      new THREE.SphereGeometry(0.48, 20, 18),
      new THREE.MeshStandardMaterial({ map: faceBuddhaTex, roughness: 0.25 })
    );
    qaHead.position.set(0, 3.8, 0);
    qaHead.rotation.y = Math.PI;
    qaGroup.add(qaHead);

    const qaHalo = addCylT(0, 3.8, -0.15, 1.5, 0.05, mat(0x48cae4, 0.1, 0, 1, 2.6), qaGroup);
    qaHalo.rotation.x = Math.PI / 2;

    qaGroup.userData = {
      isArhat: true,
      data: {
        name: "Đại Bi Quán Thế Âm Bồ Tát (Chuẩn Đề)",
        mount: "Tòa Sen Thất Bảo",
        desc: "Đức Mẹ từ bi chở che cho vạn loài chúng sinh, lắng nghe tiếng cầu xin, ban sự an lành, bảo hộ gia đình và con trẻ."
      },
      worldPos: new THREE.Vector3(-12.0, 4.0, 0)
    };
    interactiveObjects.push(qaGroup);

    // 2. Địa Tạng Vương Bồ Tát Chibi (Vách Hữu)
    const dtGroup = new THREE.Group();
    dtGroup.position.set(13.1, 0, 0);
    dtGroup.rotation.y = -Math.PI / 2;
    temple.add(dtGroup);

    addBoxT(0, 3.2, -0.4, 3.2, 6.4, 0.6, goldMat, dtGroup);
    addBoxT(0, 3.2, -0.2, 2.8, 5.8, 0.4, mat(0x9d0208), dtGroup);
    addCylT(0, 1.8, 0, 1.2, 0.6, lotusPinkMat, dtGroup);
    addBallT(0, 2.8, 0, 0.7, buddhaMat, dtGroup);
    const dtHead = new THREE.Mesh(
      new THREE.SphereGeometry(0.48, 20, 18),
      new THREE.MeshStandardMaterial({ map: faceBuddhaTex, roughness: 0.25 })
    );
    dtHead.position.set(0, 3.8, 0);
    dtHead.rotation.y = Math.PI;
    dtGroup.add(dtHead);

    addCylT(0.55, 3.2, 0.2, 0.04, 2.4, goldMat, dtGroup);
    const dtHalo = addCylT(0, 3.8, -0.15, 1.5, 0.05, mat(0xfb8500, 0.1, 0, 1, 2.6), dtGroup);
    dtHalo.rotation.x = Math.PI / 2;

    dtGroup.userData = {
      isArhat: true,
      data: {
        name: "Đại Nguyện Địa Tạng Vương Bồ Tát",
        mount: "Đế Thính Linh Thú",
        desc: "Đại nguyện từ bi cứu vớt cửu huyền thất tổ, gia trì phúc lộc trường cửu, phù hộ gia đạo an khang thịnh vượng."
      },
      worldPos: new THREE.Vector3(12.0, 4.0, 0)
    };
    interactiveObjects.push(dtGroup);


    // ---- Nhang khoanh treo trần (v5 — chi tiết thật của chánh điện) ----
    const coilMat = mat(0x8A4A2A, 0.85);
    [[-4.5, -9], [0, -10.5], [4.5, -9], [-2.2, -6.5], [2.2, -6.5]].forEach(([cx, cz]) => {
      addCylT(cx, 9.4, cz, 0.015, 1.1, coilMat); // dây treo
      for (let r = 0; r < 6; r++) {
        const ring = new THREE.Mesh(new THREE.TorusGeometry(0.52 - r * 0.055, 0.045, 8, 24), coilMat);
        ring.rotation.x = Math.PI / 2;
        ring.position.set(cx, 8.8 - r * 0.22, cz);
        ring.castShadow = false;
        temple.add(ring);
      }
      const tag = addBoxT(cx, 7.3, cz, 0.34, 0.5, 0.03, mat(0xC0392B, 0.6)); tag.castShadow = false; // thẻ đỏ dưới khoanh nhang
    });

    // ---- Chuông Pháp Bảo (cao 1,2m · nặng 150kg — để bên phải bàn thờ) ----
    const bellStand = new THREE.Group(); bellStand.position.set(9.8, 0, -12.5); temple.add(bellStand);
    addBoxT(-0.9, 1.5, 0, 0.18, 3.0, 0.18, woodDark, bellStand);
    addBoxT(0.9, 1.5, 0, 0.18, 3.0, 0.18, woodDark, bellStand);
    addBoxT(0, 3.05, 0, 2.1, 0.2, 0.3, woodDark, bellStand);
    const bellBody = addCylT(0, 2.0, 0, 0.62, 1.2, mat(0x8C6A2F, 0.35, 0.85), bellStand, 0.42);
    addCylT(0, 2.72, 0, 0.14, 0.25, mat(0x8C6A2F, 0.35, 0.85), bellStand);
    const bellSign = plaque(['CHUÔNG', 'PHÁP BẢO'], 1.7, 0.85, { w: 512, h: 256, bg: '#5A3D26', fg: '#FFD166', font: 'bold 54px Georgia, serif' });
    bellSign.position.set(0, 0.75, 0.35); bellStand.add(bellSign);

    // ---- Điện thờ Tổ (vách tây — lễ Tổ TRƯỚC khi lạy Phật) ----
    const toShrine = new THREE.Group(); toShrine.position.set(-12.6, 0, 4); toShrine.rotation.y = Math.PI / 2; temple.add(toShrine);
    addBoxT(0, 1.1, 0, 3.4, 2.2, 1.1, mat(0x5A3D26, 0.5), toShrine);
    addBoxT(0, 2.3, 0, 3.6, 0.14, 1.3, goldMat, toShrine);
    const toSign = plaque(['TỔ'], 1.1, 1.1, { w: 256, h: 256, bg: '#8E2323', fg: '#FFD166', font: 'bold 120px Georgia, serif' });
    toSign.position.set(0, 3.4, 0.3); toShrine.add(toSign);
    addCylT(-0.8, 2.55, 0.4, 0.16, 0.35, mat(0x8C5E32, 0.35, 0.8), toShrine);
    addCylT(0.8, 2.55, 0.4, 0.16, 0.35, mat(0x8C5E32, 0.35, 0.8), toShrine);

    // v8 — BỒ ĐOÀN trong điện: 6 khách quỳ thiền (module_5) trước đây ngồi
    // thẳng trên sàn (toàn module_3 không có cushion nào). Đĩa đỏ sẫm viền
    // vàng dưới đúng 6 vị trí quỳ (local temple), mặt bồ đoàn ~0,325 khớp
    // group.y = 0,32 của avatar quỳ.
    const cushionInMat8 = mat(0x7A1F1F, 0.75);
    [[-4.5, -4], [0, -4], [4.5, -4], [-4.5, 2], [0, 2], [4.5, 2]].forEach(([cx, cz]) => {
      addCylT(cx, 0.19, cz, 0.55, 0.18, cushionInMat8);
      addCylT(cx, 0.30, cz, 0.47, 0.05, mat(0x9D0208, 0.7));
      addCylT(cx, 0.12, cz, 0.58, 0.04, goldMat);
    });

    // Nội điện đặt ở không gian riêng (300, 0, 300), layer 1 (đèn riêng, tối hơn)
    temple.position.set(300, 0, 300);
    setLayerRecursive(temple, 1);
    // Đèn nội điện theo grade D2 (layer 1).
    // V6 SỬA LỖI: bản cũ ghi position bằng tọa độ WORLD trong khi đèn là con của
    // group temple (đã dời +300,+300) -> vị trí thật lệch thành (600,~600), nội
    // điện chỉ còn sáng nhờ hemisphere. Nay dùng tọa độ LOCAL của temple.
    const buddhaSpot = new THREE.SpotLight(0xffdf78, 6.5, 40, Math.PI / 3.5, 0.6);
    buddhaSpot.position.set(0, 10, -8);
    buddhaSpot.target.position.set(0, 7.5, -18.7);
    buddhaSpot.layers.set(1);
    temple.add(buddhaSpot); temple.add(buddhaSpot.target);
    const buddhaPoint = new THREE.PointLight(0xffd166, 2.6, 18);
    buddhaPoint.position.set(0, 8.5, -16.5);
    buddhaPoint.layers.set(1);
    temple.add(buddhaPoint);
    const leftWallLight = new THREE.PointLight(0xffaa00, 1.6, 38);
    leftWallLight.position.set(-10, 6.0, 0);
    leftWallLight.layers.set(1);
    temple.add(leftWallLight);
    const rightWallLight = new THREE.PointLight(0xffaa00, 1.6, 38);
    rightWallLight.position.set(10, 6.0, 0);
    rightWallLight.layers.set(1);
    temple.add(rightWallLight);
    // Nến bàn thờ: 2 đèn nến riêng (flicker ±15% ~7Hz, G5) — đặt ở phần khói/ánh sáng
    const candleLights = [];
    [-4.8, 4.8].forEach(dx => {
      const cl = new THREE.PointLight(0xffaa00, 1.0, 8);
      cl.position.set(dx, 4.4, altarZ + 1.5);
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

    function spawnBlessingText(text, x, y) {
      const el = document.createElement('div');
      el.className = 'floating-blessing';
      el.textContent = text;
      el.style.left = `${x || window.innerWidth / 2}px`;
      el.style.top = `${y || window.innerHeight / 2}px`;
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 1600);
    }
    window.spawnBlessingText = spawnBlessingText;

    // MODAL HANDLERS
    window.openModal = function(id) {
      document.getElementById(id).classList.add('open');
    };
    window.closeModal = function(id) {
      document.getElementById(id).classList.remove('open');
    };

    // v5: ĐÈN NGUYỆN THẢ HỒ đã XÓA (không có ở chùa Vĩnh Tràng thật); cửa hàng mở qua trạm/tray ở module_6b.

    // Đặt Hàng Pháp Bảo Thật
    window.orderItem = function(name, price) {
      closeModal('shop-modal');
      closeModal('arhat-modal');
      document.getElementById('order-item-title').textContent = `Thỉnh: ${name}`;
      document.getElementById('order-item-desc').textContent = `Giá gieo duyên: ${price} · Đóng gói cẩn thận, chuyển phát COD tận nhà.`;
      openModal('order-modal');
    };

    document.getElementById('btn-submit-order').onclick = () => {
      const name = document.getElementById('order-name').value.trim();
      const phone = document.getElementById('order-phone').value.trim();
      const addr = document.getElementById('order-address').value.trim();
      if (!name || !phone || !addr) {
        alert('Vui lòng điền đủ Họ tên, Số điện thoại và Địa chỉ nhận hàng.');
        return;
      }
      playBell();
      closeModal('order-modal');
      showToast('Đã ghi nhận đơn thỉnh. Nhà chùa sẽ liên hệ sớm nhất.');
      document.getElementById('so-user').textContent = name;
      setTimeout(() => openModal('so-modal'), 1200);
    };
