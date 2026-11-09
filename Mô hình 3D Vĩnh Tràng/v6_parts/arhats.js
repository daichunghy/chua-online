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

