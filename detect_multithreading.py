import os
import cv2
import concurrent.futures
from skimage.metrics import structural_similarity as ssim
import time

# Đường dẫn đến thư mục chứa các bức ảnh
path = "./images_in"

# Lấy danh sách các tệp tin ảnh trong thư mục
image_files = [os.path.join(path, f) for f in os.listdir(path) if
               os.path.isfile(os.path.join(path, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

# Hàm kiểm tra đồng bộ hóa so sánh 2 bức ảnh
def check_duplicate(img_path1, img_path2):
    # Đọc ảnh từ file
    img1 = cv2.imread(img_path1)
    img2 = cv2.imread(img_path2)

    # Chuyển ảnh sang độ xám
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Resize ảnh cùng kích thước
    img1_gray_resized = cv2.resize(img1_gray, (img2_gray.shape[1], img2_gray.shape[0]))

    # Tính toán chỉ số SSIM
    ssim_score = ssim(img1_gray_resized, img2_gray)

    # Nếu chỉ số SSIM > 0.95, coi như 2 ảnh giống nhau và trả về kết quả
    if ssim_score > 0.95:
        return (img_path1, img_path2)

# Tạo các cặp bức ảnh để so sánh
pairs = []
for i in range(len(image_files)):
    for j in range(i + 1, len(image_files)):
        pairs.append((image_files[i], image_files[j]))

# Sử dụng multithreading để so sánh các cặp ảnh
duplicates = []
start_time = time.time()
with concurrent.futures.ThreadPoolExecutor() as executor:
# with concurrent.futures.ThreadPoolExecutor(max_workers=10000) as executor:
    # Tạo các task và submit chúng vào thread pool
    futures = [executor.submit(check_duplicate, pair[0], pair[1]) for pair in pairs]

    # Lấy kết quả trả về từ các task đã hoàn thành
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result is not None:
            duplicates.append(result)
end_time = time.time()

# In ra danh sách các bức ảnh trùng lặp
if duplicates:
    print("Các bức ảnh trùng lặp:")
    for dup in duplicates:
        print(dup[0], dup[1])
else:
    print("Không có bức ảnh trùng lặp trong thư mục này.")

print("Thời gian thực hiện: ", end_time - start_time, "giây")
