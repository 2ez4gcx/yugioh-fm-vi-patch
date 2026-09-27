# Yu-Gi-Oh! Forbidden Memories — bản dịch tiếng Việt

Bản vá (patch) Việt hoá cho trò chơi PlayStation 1 *Yu-Gi-Oh! Forbidden
Memories* (Konami, bản Mỹ phát hành năm 2002, mã đĩa **SLUS-01411**).

Đây là dự án của người hâm mộ, không liên quan tới Konami. Gói này **không
chứa** đĩa gốc hay bất kỳ dữ liệu nào của trò chơi. Bạn cần có ảnh đĩa gốc của
chính mình; bản vá chỉ ghi phần chữ tiếng Việt, phông chữ và vài byte mã điều
chỉnh lên ảnh đĩa đó.

Nội dung gói:

| File | Dùng để |
|---|---|
| `yugioh-fm-vi.ppf` | Bản vá, định dạng PPF 3.0 (chuẩn quen thuộc cho PS1) |
| `apply_patch.py` | Trình áp vá bằng Python, tự kiểm SHA-256 trước và sau, tự tạo `.cue` |
| `tao_cue.bat` | Tạo file `.cue` đúng tên cho file `.bin` (kéo thả hoặc nháy đúp) |
| `README.md` | Hướng dẫn này |

**Đã dịch:** mô tả của cả 722 lá bài, toàn bộ cốt truyện và hội thoại, thông báo
hệ thống, loại bài, sao hộ mệnh, danh hiệu, địa danh trên bản đồ, các nút menu,
màn tiêu đề, banner Đấu tự do, tên địa hình trong trận đấu. Chữ có dấu đầy đủ,
phông chữ vẽ lại với độ rộng chữ thay đổi theo từng ký tự.

**Giữ tiếng Anh có chủ đích:** tên lá bài (để dễ tra cứu, trao đổi mật mã),
WIN / LOSE, WINNER, LP, COM / YOU, thanh CHEST / ORDER ở màn xếp bài, nút END ở
màn nhập tên, bảng luật đấu 2 người (chữ vẽ sẵn trong hình).

**Chưa kiểm tra trực tiếp trong game:** các hộp thoại chỉ hiện khi thẻ nhớ gặp
vấn đề (ghi đè, định dạng…), bảng luật đấu 2 người, và 6 tên địa hình chỉ hiện
khi đánh lá bài địa hình (đã kiểm bằng ảnh ghép từ dữ liệu game). Gặp lỗi ở các
chỗ này xin báo lại theo mục 8.

---

## Hình ảnh

| | |
|---|---|
| ![Màn tiêu đề](docs/anh/01-man-tieu-de.png) | ![Menu tiêu đề](docs/anh/02-menu-tieu-de.png) |
| Màn tiêu đề | Menu tiêu đề, hộp thoại Tải |
| ![Cốt truyện](docs/anh/03-cot-truyen.png) | ![Lựa chọn](docs/anh/04-lua-chon.png) |
| Cốt truyện | Lựa chọn trong hội thoại |
| ![Trận đấu](docs/anh/05-tran-dau.png) | ![Đấu tự do](docs/anh/06-dau-tu-do.png) |
| Trận đấu | Đấu tự do |
| ![Thư viện](docs/anh/07-thu-vien.png) | |
| Mô tả lá bài trong Thư viện | |

## 1. Chuẩn bị ảnh đĩa gốc

Bạn cần ảnh đĩa dạng **`.bin` + `.cue`** (Mode 2, 2352 byte mỗi sector) của
đĩa Mỹ SLUS-01411. Đây là định dạng mà các phần mềm đọc đĩa PS1 phổ biến
(ImgBurn, CDRDAO, Alcohol 120%…) xuất ra khi chọn kiểu "BIN/CUE". Một số lưu ý:

- Ảnh đĩa phải có **đúng một file `.bin`**. Nếu `.cue` của bạn liệt kê nhiều
  file (Track 01, Track 02…), đó là kiểu chia track, không dùng trực tiếp được.
- File `.iso` (2048 byte mỗi sector) **không** dùng được: bản vá tính theo
  sector 2352 byte có mã sửa lỗi.
- Kích thước đúng của `.bin`: **517.872.768 byte** (220.184 sector).

Bản vá được tạo từ đúng một ảnh đĩa; ảnh khác dù "cùng game" cũng có thể lệch
vài byte. Vì vậy phải kiểm SHA-256 trước khi áp.

## 2. Kiểm SHA-256 của ảnh đĩa gốc

SHA-256 là "dấu vân tay" của file: hai file giống nhau từng byte thì ra cùng
một chuỗi 64 ký tự. Ảnh đĩa gốc phải cho ra đúng:

```
6e22494a45bf50fa2d239cd3819a57163a5f9b91e0365babc3e101509b5c3a7c
```

Cách tính trên từng hệ điều hành (thay `TEN_FILE.bin` bằng tên file của bạn;
nếu đường dẫn có khoảng trắng thì đặt trong dấu ngoặc kép):

**Windows, dùng Command Prompt (cmd):**

```
certutil -hashfile "TEN_FILE.bin" SHA256
```

Mở cmd bằng cách gõ `cmd` vào ô tìm kiếm của Start; dùng lệnh `cd` để vào thư
mục chứa file, hoặc kéo thả file vào cửa sổ cmd để dán đường dẫn. Kết quả hiện
ở dòng thứ hai, có thể có khoảng trắng giữa các cặp ký tự, cứ bỏ khoảng trắng
mà so.

**Windows, dùng PowerShell:**

```
Get-FileHash "TEN_FILE.bin" -Algorithm SHA256
```

Cột `Hash` là kết quả (chữ in hoa, so không phân biệt hoa thường).

**macOS (Terminal):**

```
shasum -a 256 "TEN_FILE.bin"
```

**Linux:**

```
sha256sum "TEN_FILE.bin"
```

File khoảng 500 MB nên tính mất chừng mười giây. Chỉ cần so **8 ký tự đầu** là
đủ để nhận ra: đĩa gốc đúng bắt đầu bằng `6e22494a`. Nếu khác, xem mục 6.

## 3. Áp vá — cách 1: PPF-O-Matic (Windows, không cần cài gì)

PPF-O-Matic là công cụ nhỏ, miễn phí, chuyên áp bản vá PPF cho đĩa PS1; tìm
"PPF-O-Matic 3" trên các trang lưu trữ công cụ ROM hacking.

1. **Sao chép** file `.bin` gốc ra một bản khác, ví dụ `yugioh-fm-vi.bin`.
   PPF-O-Matic sửa thẳng vào file được chọn, nên luôn giữ lại bản gốc.
2. Mở PPF-O-Matic. Ô **ISO file**: chọn bản sao vừa tạo. Ô **Patch**: chọn
   `yugioh-fm-vi.ppf`.
3. Bấm **Apply**. Chỉ vài giây, chương trình báo "Successfully patched".
4. Kiểm lại theo mục 5.

## 4. Áp vá — cách 2: Python (Windows, macOS, Linux)

Cần Python 3 (tải từ python.org; trên Windows khi cài nhớ tick "Add Python to
PATH"). Cách này **không sửa** file gốc mà tạo file mới, và tự kiểm SHA-256.

1. Đặt `apply_patch.py`, `yugioh-fm-vi.ppf` và file `.bin` gốc vào cùng một
   thư mục.
2. Mở cmd / PowerShell / Terminal tại thư mục đó và chạy:

```
python apply_patch.py "TEN_FILE_GOC.bin" yugioh-fm-vi.ppf yugioh-fm-vi.bin
```

(Trên macOS/Linux nếu `python` không có thì dùng `python3`.)

3. Kịch bản kiểm SHA-256 của file gốc trước; nếu không đúng nó dừng lại và báo
   "Dia goc khong dung". Nếu đúng, nó ghi ra `yugioh-fm-vi.bin`, in SHA-256
   của file mới và báo `KHOP ban phat hanh` khi kết quả chuẩn.
4. Kịch bản **tự tạo luôn `yugioh-fm-vi.cue`** cạnh file `.bin`, đúng tên,
   nên bỏ qua bước tạo `.cue` bằng tay ở mục 5.

## 5. Kiểm kết quả

Tính SHA-256 của file đã vá (cùng cách ở mục 2). Kết quả đúng:

```
685e55bf71ab376ec8d2a6390403e7902e2aa42f2171af578af02aa662f536ca
```

Tức là bắt đầu bằng `685e55bf`. Đúng chuỗi này thì file của bạn giống từng
byte với bản đã được kiểm thử; mọi lỗi nếu có sẽ không phải do bước áp vá.

Nếu áp bằng PPF-O-Matic thì cần thêm file `.cue` cho đĩa mới (cách Python đã
tự tạo sẵn). Nhanh nhất: **kéo thả file `.bin` đã vá lên `tao_cue.bat`**, hoặc
chép `tao_cue.bat` vào cùng thư mục rồi nháy đúp — nó tạo `.cue` đúng tên cho
mọi file `.bin` ở đó. Muốn làm tay thì sao chép file `.cue` gốc, đổi tên thành
`yugioh-fm-vi.cue`, mở bằng Notepad và sửa tên file `.bin` ở dòng đầu cho
khớp. Nội dung chuẩn chỉ có ba dòng:

```
FILE "yugioh-fm-vi.bin" BINARY
  TRACK 01 MODE2/2352
    INDEX 01 00:00:00
```

## 6. Khi SHA-256 không khớp

- **Ảnh gốc ra chuỗi khác `6e22494a…`:** ảnh đĩa của bạn không phải bản mà bản
  vá được tạo từ đó. Nguyên nhân hay gặp: đọc đĩa ra kiểu `.iso` 2048 byte
  (kích thước sẽ nhỏ hơn 500 MB nhiều), đọc thiếu hoặc thừa sector cuối, đĩa
  thuộc bản in khác (bản châu Âu SLES có dữ liệu khác, không dùng được), hoặc file
  từng bị áp một bản vá khác. Cách chắc nhất là đọc lại từ đĩa thật bằng
  ImgBurn ở chế độ BIN/CUE. Bản vá áp lên ảnh sai vẫn chạy được phần lớn,
  nhưng có thể lỗi ở chỗ không lường trước.
- **Ảnh đã vá ra chuỗi khác `685e55bf…`:** bạn đã áp lên ảnh gốc sai (xem
  trên), hoặc áp lên file đã bị sửa khác. Làm lại từ bản sao gốc.

## 7. Chạy trên giả lập

Mở file **`.cue`** (không phải `.bin`) bằng giả lập. Đã thử trên PCSX-Redux;
DuckStation, ePSXe, Mednafen/Beetle PSX đều đọc được BIN/CUE.

- Thẻ nhớ (save trong game) dùng bình thường, kể cả save từ bản tiếng Anh:
  bản vá không đổi cấu trúc dữ liệu lưu, lá bài và mật mã giữ nguyên.
- **Không nạp save state** (lưu nhanh của giả lập, kiểu F5/F7) được tạo trên
  bản tiếng Anh: save state giữ nguyên toàn bộ bộ nhớ lúc lưu, nên vẫn hiện chữ
  cũ dù đĩa mới đã đúng. Vào game bằng "Tiếp tục" từ thẻ nhớ.
- Mật mã lá bài (8 chữ số) giữ nguyên như bản gốc, tra cứu theo tên tiếng Anh.

## 8. Câu hỏi thường gặp

**Có thể dùng bản vá xdelta không?** Gói này phát hành PPF vì là chuẩn lâu năm
cho PS1. Ai có sẵn hai ảnh đĩa có thể tự tạo xdelta bằng xdelta UI, kết quả
tương đương.

**Tại sao phải kiểm SHA-256 kỹ vậy?** Vì các lỗi khó chịu nhất (đứng máy, mất
chữ) thường bắt nguồn từ chỉ vài byte lệch. Kiểm hash là cách duy nhất biết
chắc file của bạn giống file đã được thử.

**Báo lỗi ở đâu?** Mở issue trên repo này, kèm: SHA-256 của file đã vá, tên
giả lập, và ảnh chụp màn hình cùng câu thoại cuối cùng trước khi lỗi.

## 9. Bản quyền

Trò chơi, tên gọi, hình ảnh và âm thanh thuộc Konami và các chủ sở hữu liên
quan. Bản vá chỉ chứa phần chữ dịch, phông chữ vẽ lại và các byte mã điều
chỉnh, không phân phối dữ liệu gốc. Nếu chủ sở hữu bản quyền yêu cầu, bản vá
sẽ được gỡ.

---

Bản dịch do **Khuong Doan** thực hiện — <https://khuongdoan.com/>

<sub>Bản vá miễn phí và sẽ luôn như vậy. Nếu nó giúp bạn chơi lại trò chơi tuổi thơ và bạn muốn mời tác giả một ly cà phê, quét mã MoMo bên dưới. Không bắt buộc, không kèm quyền lợi gì thêm.</sub>

<a href="https://github.com/2ez4gcx/Project-hub/blob/main/docs/anh/ung-ho-momo.png"><img src="https://raw.githubusercontent.com/2ez4gcx/Project-hub/main/docs/anh/ung-ho-momo.png" alt="Ủng hộ tác giả qua MoMo" width="170"></a>
