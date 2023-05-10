# import os
# import cv2
# import concurrent.futures
# from skimage.metrics import structural_similarity as ssim
# import time
#
# # Đường dẫn đến thư mục chứa các bức ảnh
# path = "./data"
#
# # Lấy danh sách các tệp tin ảnh trong thư mục
# image_files = [os.path.join(path, f) for f in os.listdir(path) if
#                os.path.isfile(os.path.join(path, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
#
# # Số lượng ảnh tối đa cần so sánh
# max_images = len(image_files)
# def check_duplicate(img_path1, img_path2):
#     # Đọc ảnh từ file
#     img1 = cv2.imread(img_path1)
#     img2 = cv2.imread(img_path2)
#
#     # Chuyển ảnh sang độ xám
#     img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#     img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#
#     # Resize ảnh cùng kích thước
#     img1_gray_resized = cv2.resize(img1_gray, (img2_gray.shape[1], img2_gray.shape[0]))
#
#     # Tính toán chỉ số SSIM
#     ssim_score = ssim(img1_gray_resized, img2_gray)
#
#     # Nếu chỉ số SSIM > 0.95, coi như 2 ảnh giống nhau và trả về kết quả
#     if ssim_score > 0.95:
#         return (img_path1, img_path2)
#
# # Thực hiện so sánh từng cặp ảnh với số lượng ảnh từ 1 đến max_images
# for num_images in range(1, max_images + 1):
#     # Tạo các cặp bức ảnh để so sánh
#     pairs = []
#     for i in range(num_images):
#         for j in range(i + 1, num_images):
#             pairs.append((image_files[i], image_files[j]))
#
#     # Sử dụng multithreading để so sánh các cặp ảnh
#     duplicates = []
#     start_time = time.time()
#     # with concurrent.futures.ThreadPoolExecutor() as executor:
#     with concurrent.futures.ThreadPoolExecutor(max_workers=99999) as executor:
#         # Tạo các task và submit chúng vào thread pool
#         futures = [executor.submit(check_duplicate, pair[0], pair[1]) for pair in pairs]
#
#         # Lấy kết quả trả về từ các task đã hoàn thành
#         for future in concurrent.futures.as_completed(futures):
#             result = future.result()
#             if result is not None:
#                 duplicates.append(result)
#     end_time = time.time()
#
#     # In ra thời gian thực hiện
#     print("Thời gian chạy với", num_images, "ảnh:", end_time - start_time, "giây")

import os
import cv2
import concurrent.futures
from skimage.metrics import structural_similarity as ssim
import time
import matplotlib.pyplot as plt

# Đường dẫn đến thư mục chứa các bức ảnh
path = "./data"

# Lấy danh sách các tệp tin ảnh trong thư mục
image_files = [os.path.join(path, f) for f in os.listdir(path) if
               os.path.isfile(os.path.join(path, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

# Khởi tạo các giá trị số lượng ảnh để tính toán thời gian thực hiện và vẽ biểu đồ
max_num_images = len(image_files)
num_images = []
execution_times = []
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
# Lặp qua các số lượng ảnh khác nhau để tính toán thời gian thực hiện và lưu vào num_images và execution_times
for num in range(1, max_num_images+1):
    pairs = []
    for i in range(num):
        for j in range(i + 1, num):
            pairs.append((image_files[i], image_files[j]))

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
    # with concurrent.futures.ThreadPoolExecutor(max_workers=1000000) as executor:
        # Tạo các task và submit chúng vào thread pool
        futures = [executor.submit(check_duplicate, pair[0], pair[1]) for pair in pairs]

        # Lấy kết quả trả về từ các task đã hoàn thành
        for future in concurrent.futures.as_completed(futures):
            result = future.result()

    end_time = time.time()
    num_images.append(num)
    execution_times.append(end_time - start_time)

# Vẽ biểu đồ dữ liệu
plt.plot(num_images, execution_times)
plt.xlabel("Số lượng ảnh")
plt.ylabel("Thời gian thực hiện (giây)")
plt.show()
