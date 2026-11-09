    // MODAL HANDLERS
    window.openModal = function(id) {
      document.getElementById(id).classList.add('open');
    };
    window.closeModal = function(id) {
      document.getElementById(id).classList.remove('open');
    };

    document.getElementById('btn-release-lamp').onclick = () => openModal('lamp-modal');
    document.getElementById('btn-open-shop').onclick = () => openModal('shop-modal');
    document.getElementById('btn-open-so').onclick = () => openModal('so-modal');

    // Thả Đèn Nguyện Cầu An
    document.getElementById('btn-confirm-lamp').onclick = () => {
      const name = document.getElementById('lamp-user-name').value.trim() || 'Phật tử ẩn danh';
      const text = document.getElementById('lamp-prayer-text').value.trim() || 'Nguyện cầu gia đạo an khang thịnh vượng, vạn sự hanh thông';

      playBell();
      closeModal('lamp-modal');

      const list = document.getElementById('prayer-list');
      const card = document.createElement('div');
      card.className = 'prayer-card';
      card.style.borderColor = '#ffd166';
      card.innerHTML = `
        <div class="prayer-text">"${text}"</div>
        <div class="prayer-meta">
          <span class="prayer-user">✨ ${name}</span>
          <span>Vừa thắp · 1 kính bái</span>
        </div>
      `;
      list.prepend(card);

      spawnBlessingText('🏮 Đèn Nguyện Đã Thắp Sáng Bàn Tam Bảo!', window.innerWidth / 2, window.innerHeight * 0.4);
      showToast(`🏮 Ngọn đèn cầu an của ${name} đã được thắp sáng trên Chánh Điện!`);
    };

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
      showToast('🎉 Đã ghi nhận đơn thỉnh pháp bảo! Nhà chùa sẽ liên hệ sớm nhất.');
      document.getElementById('so-user').textContent = name;
      setTimeout(() => openModal('so-modal'), 1200);
    };

