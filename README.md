# BizMaC N8N Manager

BizMaC N8N Manager là bộ công cụ dòng lệnh giúp cài đặt và quản lý N8N trên máy chủ Ubuntu. Công cụ tự động cấu hình Docker, PostgreSQL, Redis, Nginx, SSL Let's Encrypt và cung cấp các thao tác quản trị thường dùng.

> Lệnh chính là `bizmac-n8n`. `n8n-host` chỉ là alias tương thích với các bản cài đặt trước.

## Yêu cầu hệ thống

- Ubuntu 20.04, 22.04 hoặc 24.04
- Quyền quản trị `root`/`sudo`
- Tên miền đã trỏ bản ghi DNS về IP public của máy chủ
- Cấu hình tối thiểu: 1 CPU, 1 GB RAM, 20 GB lưu trữ
- Cấu hình khuyến nghị: 2 CPU, 2 GB RAM, 20 GB lưu trữ trở lên

## Cài đặt

### Cách 1: Clone repository

```bash
git clone https://github.com/davidthuong/n8n-panel.git
cd n8n-panel
sudo bash install.sh
```

### Cách 2: Tải installer trực tiếp

```bash
curl -fsSL https://raw.githubusercontent.com/davidthuong/n8n-panel/main/install.sh -o install.sh
sudo bash install.sh
```

Installer sẽ:

1. Tải script quản trị `n8n-host.sh` từ repository này.
2. Cài lệnh chính tại `/usr/local/bin/bizmac-n8n`.
3. Tạo alias tương thích `/usr/local/bin/n8n-host`.
4. Tải workflow import vào `/n8n-templates/import-workflow-credentials.json`.

### Nguồn asset cài đặt

GitHub hiện là nguồn asset tạm thời. Installer lấy script quản trị và template từ biến `ASSET_BASE_URL`, với giá trị mặc định là repository này.

Khi hạ tầng download BizMaC sẵn sàng, có thể chuyển nguồn mà không sửa installer:

```bash
sudo env BIZMAC_ASSET_BASE_URL="<URL_ASSET_BIZMAC>" bash install.sh
```

URL được cung cấp phải có cấu trúc:

```text
<URL_ASSET_BIZMAC>/n8n-host.sh
<URL_ASSET_BIZMAC>/templates/import-workflow-credentials.json
```

## Sử dụng

Mở menu quản trị:

```bash
sudo bizmac-n8n
```

Hiển thị trợ giúp:

```bash
bizmac-n8n --help
```

Lệnh cũ `n8n-host` vẫn hoạt động và chuyển tới cùng công cụ.

### Chức năng chính

| Số | Chức năng |
| --- | --- |
| 1 | Cài đặt N8N |
| 2 | Thay đổi tên miền |
| 3 | Nâng cấp N8N lên image `latest` |
| 4 | Tắt xác thực hai bước (2FA/MFA) cho tài khoản |
| 5 | Đặt lại tài khoản owner |
| 6 | Export workflows và credentials |
| 7 | Import workflow hỗ trợ khôi phục dữ liệu |
| 8 | Hiển thị thông tin kết nối Redis |
| 9 | Quản lý NocoDB |
| 10 | Xóa toàn bộ N8N và cài đặt lại |

## Luồng cài đặt N8N

Khi chọn `1) Cài đặt N8N`, công cụ sẽ:

1. Cài các gói cần thiết: Docker, Docker Compose, Nginx, Certbot, DNS utilities và cURL.
2. Kiểm tra DNS của tên miền.
3. Tạo thông tin xác thực ngẫu nhiên cho PostgreSQL, Redis và khóa mã hóa N8N.
4. Tạo Docker Compose với N8N, PostgreSQL và Redis.
5. Cấu hình reverse proxy Nginx và chứng chỉ SSL Let's Encrypt.
6. Kiểm tra khả năng truy cập N8N qua HTTPS.

Dữ liệu và cấu hình được lưu tại `/n8n-cloud`. Hãy sao lưu file `/n8n-cloud/.env` ở nơi an toàn vì file này chứa khóa mã hóa và thông tin xác thực.

## Export và import dữ liệu

### Export

Chọn mục `6` để xuất toàn bộ workflows và credentials. Các file được lưu trong `/n8n-cloud/backups` và được cung cấp qua đường dẫn HTTPS tạm thời trong phiên làm việc.

### Import

Chọn mục `7` để import workflow `[BizMaC] Import Workflows, Credentials`. Sau khi import:

1. Mở workflow trong giao diện N8N.
2. Kích hoạt workflow.
3. Mở Production URL của Form Trigger.
4. Tải lên file workflows hoặc credentials đã export.

## Quản lý NocoDB

Chọn mục `9` để mở menu NocoDB:

- Khi chưa cài đặt: chọn `1` để cài đặt.
- Khi đã cài đặt: chọn `1` để xem thông tin, `2` để khởi động lại, hoặc `3` để gỡ cài đặt.

## Gỡ công cụ quản trị

```bash
sudo bizmac-n8n --uninstall
```

Lệnh này xóa cả `/usr/local/bin/bizmac-n8n` và alias `/usr/local/bin/n8n-host`; dữ liệu N8N trong `/n8n-cloud` không bị xóa.

## Cảnh báo an toàn

- Mục `10) Xóa N8N và cài đặt lại` xóa vĩnh viễn workflows, credentials, executions, PostgreSQL, Redis, cấu hình Nginx và chứng chỉ SSL liên quan. Hãy export dữ liệu trước khi sử dụng.
- Mục `8) Lấy thông tin Redis` hiển thị mật khẩu Redis trên terminal. Không chia sẻ nội dung này.
- File `.env` chứa dữ liệu nhạy cảm và phải được bảo vệ bằng quyền truy cập phù hợp.

## Tình trạng giấy phép

Kiểm tra ngày 13/07/2026 cho thấy:

- [`davidthuong/n8n-panel`](https://github.com/davidthuong/n8n-panel) là fork trực tiếp của [`vvthien/n8n-panel`](https://github.com/vvthien/n8n-panel), không phải một codebase độc lập.
- Cả repository hiện tại và upstream đều không có file `LICENSE`; GitHub API cũng không nhận diện giấy phép cho hai repository.
- Repository công khai và khả năng fork trên GitHub không tự động cấp quyền sửa đổi, phân phối, white-label hoặc thương mại hóa mã nguồn.
- Trước khi bán, phân phối hoặc cung cấp dịch vụ dựa trên bản chỉnh sửa này, cần có sự cho phép bằng văn bản từ chủ sở hữu quyền tác giả thực tế, hoặc thay thế bằng một bản triển khai clean-room có giấy phép rõ ràng.
- N8N được triển khai bởi script có lớp giấy phép riêng. Hãy kiểm tra [n8n Sustainable Use License](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) và [hướng dẫn use case chính thức](https://support.n8n.io/article/can-i-use-your-license-for-my-use-case); dịch vụ managed hosting hoặc white-label có thể yêu cầu Enterprise/Embed license.

Nội dung trên là ghi nhận kỹ thuật về trạng thái license, không phải tư vấn pháp lý. Không thêm một license mới vào repository này nếu chưa xác minh quyền cấp phép.

## Kiểm tra mã nguồn

```bash
python -m unittest discover -v
bash -n install.sh n8n-host.sh
python -m json.tool templates/import-workflow-credentials.json > /dev/null
```

## Mã nguồn

- Repository: https://github.com/davidthuong/n8n-panel
- Thương hiệu giao diện quản trị: **BizMaC**
