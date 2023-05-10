import os
import cv2
from skimage.metrics import structural_similarity as ssim
import time

# Đường dẫn đến thư mục chứa các bức ảnh
path = "./data"

# Lấy danh sách các tệp tin ảnh trong thư mục
image_files = [os.path.join(path, f) for f in os.listdir(path) if
               os.path.isfile(os.path.join(path, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

# Sắp xếp danh sách các tệp tin ảnh theo thứ tự tên tệp
image_files.sort()

# Danh sách các bức ảnh trùng lặp
duplicates = []

for num_images in range(1, len(image_files) + 1):
    start_time = time.time()  # Lấy thời điểm bắt đầu chạy code

    # So sánh các cặp ảnh trong danh sách
    for i in range(len(image_files)):
        for j in range(i + 1, num_images):
            # Đọc ảnh từ file
            img1 = cv2.imread(image_files[i])
            img2 = cv2.imread(image_files[j])

            # Chuyển ảnh sang độ xám
            img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            # Resize ảnh cùng kích thước
            img1_gray_resized = cv2.resize(img1_gray, (img2_gray.shape[1], img2_gray.shape[0]))

            # Tính toán chỉ số SSIM
            ssim_score = ssim(img1_gray_resized, img2_gray)

            # Nếu chỉ số SSIM > 0.95, coi như 2 ảnh giống nhau và lưu vào danh sách các bức ảnh trùng lặp
            if ssim_score > 0.95:
                duplicates.append((image_files[i], image_files[j]))

    end_time = time.time()  # Lấy thời điểm kết thúc chạy code
    elapsed_time = end_time - start_time  # Tính thời gian chạy code

    # In ra số lượng ảnh so sánh và thời gian thực hiện tương ứng
    print("Số lượng ảnh: %d - Thời gian thực hiện: %.2f giây" % (num_images, elapsed_time))

    # Đặt lại danh sách các bức ảnh trùng lặp để tiến hành cho đến hết
    duplicates = []

# import os
# import cv2
# from skimage.metrics import structural_similarity as ssim
# import time
# import matplotlib.pyplot as plt
#
# # Đường dẫn đến thư mục chứa các bức ảnh
# path = "./data"
#
# # Lấy danh sách các tệp tin ảnh trong thư mục
# image_files = [os.path.join(path, f) for f in os.listdir(path) if               os.path.isfile(os.path.join(path, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
#
# # Sắp xếp danh sách các tệp tin ảnh theo thứ tự tên tệp
# image_files.sort()
#
# # Danh sách các bức ảnh trùng lặp
# duplicates = []
#
# # Khởi tạo mảng x và y
# x = []
# y = []
#
# for num_images in range(1, len(image_files) + 1):
#     start_time = time.time()  # Lấy thời điểm bắt đầu chạy code
#
#     # So sánh các cặp ảnh trong danh sách
#     for i in range(len(image_files)):
#         for j in range(i + 1, num_images):
#             # Đọc ảnh từ file
#             img1 = cv2.imread(image_files[i])
#             img2 = cv2.imread(image_files[j])
#
#             # Chuyển ảnh sang độ xám
#             img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#             img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#
#             # Resize ảnh cùng kích thước
#             img1_gray_resized = cv2.resize(img1_gray, (img2_gray.shape[1], img2_gray.shape[0]))
#
#             # Tính toán chỉ số SSIM
#             ssim_score = ssim(img1_gray_resized, img2_gray)
#
#             # Nếu chỉ số SSIM > 0.95, coi như 2 ảnh giống nhau và lưu vào danh sách các bức ảnh trùng lặp
#             if ssim_score > 0.95:
#                 duplicates.append((image_files[i], image_files[j]))
#
#     end_time = time.time()  # Lấy thời điểm kết thúc chạy code
#     elapsed_time = end_time - start_time  # Tính thời gian chạy code
#
#     # Lưu số lượng ảnh và thời gian thực hiện vào mảng x và y
#     x.append(num_images)
#     y.append(elapsed_time)
#
#     # Đặt lại danh sách các bức ảnh trùng lặp để tiến hành cho đến hết
#     duplicates = []
#
# # Vẽ biểu đồ thời gian thực hiện
# plt.plot(x, y)
# plt.xlabel('Số lượng ảnh')
# plt.ylabel('Thời gian thực hiện (giây)')
# plt.show()

