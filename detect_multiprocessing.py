# import os
# import cv2
# from skimage.metrics import structural_similarity as ssim
# import time
# from multiprocessing import Pool, cpu_count
#
# # Đường dẫn đến thư mục chứa các bức ảnh
# path = "./images_in"
# # Lấy danh sách các tệp tin ảnh trong thư mục
# image_files = [os.path.join(path, f) for f in os.listdir(path) if
#                os.path.isfile(os.path.join(path, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
# # Danh sách các bức ảnh trùng lặp
# duplicates = []
#
# def compare_images(pair):
#     i, j = pair
#     # Đọc ảnh từ file
#     img1 = cv2.imread(image_files[i])
#     img2 = cv2.imread(image_files[j])
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
#     # Nếu chỉ số SSIM > 0.95, coi như 2 ảnh giống nhau và lưu vào danh sách các bức ảnh trùng lặp
#     if ssim_score > 0.95:
#         return (image_files[i], image_files[j])
#     return None
#
# if __name__ == '__main__':
#     start_time = time.time()  # Lấy thời điểm bắt đầu chạy code
#     pairs = [(i, j) for i in range(len(image_files)) for j in range(i + 1, len(image_files))]
#     with Pool(processes=cpu_count()) as pool:
#         results = pool.map(compare_images, pairs)
#     duplicates = [res for res in results if res is not None]
#
#     end_time = time.time()  # Lấy thời điểm kết thúc chạy code
#     elapsed_time = end_time - start_time  # Tính thời gian chạy code
#
#     # In ra danh sách các bức ảnh trùng lặp
#     if duplicates:
#         print("Các bức ảnh trùng lặp:")
#         for dup in duplicates:
#             print(dup[0], dup[1])
#     else:
#         print("Không có bức ảnh trùng lặp trong thư mục này.")
#
#     print("Thời gian chạy code: %.2f giây" % elapsed_time)

import os
import cv2
import time
from multiprocessing import Pool, cpu_count


path = "./images_in"
image_files = [os.path.join(path, f) for f in os.listdir(path) if
os.path.isfile(os.path.join(path, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
duplicates = []

def compare_images(pair):
    i, j = pair
    # Đọc ảnh từ file
    img1 = cv2.imread(image_files[i])
    img2 = cv2.imread(image_files[j])
    # Tính toán chỉ số SSIM
    ssim_score = cv2.compareHist(cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256]),
                                 cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256]),
                                 cv2.HISTCMP_CORREL)

    if ssim_score > 0.95:
        return (image_files[i], image_files[j])
    return None

if __name__ == '__main__':
    start_time = time.time() #
    pairs = [(i, j) for i in range(len(image_files)) for j in range(i + 1, len(image_files))]
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(compare_images, pairs)
    duplicates = [res for res in results if res is not None]
    end_time = time.time()
    elapsed_time = end_time - start_time  # Tính thời gian chạy code

    # In ra danh sách các bức ảnh trùng lặp
    if duplicates:
        print("Các bức ảnh trùng lặp:")
        for dup in duplicates:
            print(dup[0], dup[1])
    else:
        print("Không có bức ảnh trùng lặp trong thư mục này.")

    print("Thời gian chạy code: %.2f giây" % elapsed_time)
print(cpu_count())
