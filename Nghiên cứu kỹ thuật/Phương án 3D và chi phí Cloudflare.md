# Phương án 3D và chi phí Cloudflare

Ngày 04/11/2026. Đây là phương án nghiên cứu, chưa triển khai hoặc kiểm thử tải.

Niệm Phật Online dùng Three.js WebGLRenderer để dựng cảnh trên thiết bị và WebSocket để trao đổi trạng thái. Mã công khai kiểm tra trạng thái 200 ms một lần, chỉ gửi khi thay đổi hoặc gửi định kỳ khi đứng yên. Client nhận thay đổi trạng thái và dữ liệu nhị phân. Nguồn: https://niemphat.online/js/world.js và https://niemphat.online/js/main.js. Không xác minh được máy chủ hoặc hóa đơn của họ.

Cyber Sansa cho biết họ dùng Cloudflare Workers, nhiều phòng với giới hạn mềm. Nguồn: https://dev.to/sansatemple_live/cyber-sansa-sansatemplelive-a-browser-3d-temple-with-multiplayer-halls-50nk

Định hướng Chùa Online là chạy cảnh 3D cartoon trên trình duyệt, tải từng khu vực, dùng R2 và CDN cho tài nguyên, Durable Objects với WebSocket để đồng bộ các phòng. Chỉ truyền trạng thái thay đổi, nội suy chuyển động ở máy người dùng và giảm gửi khi đứng yên. Những điều này là đề xuất, phải đo độ mượt, thời gian tải và khả năng tiếp cận. Không tự ý ngắt người đang thực hành yên lặng. Tôn trọng yêu cầu ngôi chùa có thật và thẩm định kiến trúc.

Phép tính Cloudflare giả định 300 người liên tục trong 8 giờ/ngày, 30 ngày, 10 phòng có 30 người, 10 Durable Objects đều hoạt động suốt thời gian trên. Bao gồm 9.000 kết nối mới/tháng. Theo giá hiện hành, Workers Paid tối thiểu $5/tháng. Durable Objects có 1 triệu request/tháng, tiếp theo $0,15/triệu và 400.000 GB-giây, tiếp theo $12,50/triệu GB-giây, làm tròn phần vượt theo đơn vị triệu. Cứ 20 tin WebSocket đi vào tính một request, không tính request cho tin gửi ra. Một Object được tính 0,128 GB. Nguồn https://developers.cloudflare.com/durable-objects/platform/pricing/ và https://developers.cloudflare.com/workers/platform/pricing/.

Với 1 tin/người/giây, 259,2 triệu tin, quy đổi 12,96 triệu request, cộng 9.000 kết nối, trừ 1 triệu miễn phí, làm tròn 12 triệu request, phí $1,80. Thời gian 10 × 8 × 3600 × 30 × 0,128 = 1.105.920 GB-giây, trừ 400.000 miễn phí và làm tròn lên 1 triệu GB-giây, phí $12,50. Tổng $19,30/tháng.

Với 5 tin/người/giây, 1,296 tỷ tin, quy đổi 64,8 triệu request, cộng 9.000 kết nối, trừ 1 triệu, làm tròn 64 triệu request, phí $9,60. Thời gian vẫn $12,50. Tổng $27,10/tháng. Con số là kịch bản giả định trên Cloudflare cho một sản phẩm tương tự, không phải chi phí thực của Niệm Phật Online, không bao gồm các chi phí khác hay thuế.

R2 Standard miễn phí 10 GB-tháng, 1 triệu thao tác Class A và 10 triệu Class B mỗi tháng, miễn phí egress; vượt mức có chi phí. Nguồn https://developers.cloudflare.com/r2/pricing/. Cần kiểm tra hành vi cache, giới hạn dịch vụ, chi phí database, domain, audio và giám sát.

Bước kiểm chứng: làm một lát cắt chùa Vĩnh Tràng, đo tổng tải lần đầu thực tế và trên mạng di động, RAM, FPS và nhiệt máy; kiểm thử 300 kết nối đồng thời theo các tình huống đứng yên, di chuyển, vào cùng lúc và trở lại; đo chi phí thực, điều chỉnh số người mỗi phòng và nhịp cập nhật. Không coi các con số dự kiến là cam kết.
