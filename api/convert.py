import base64
from datetime import date
from io import BytesIO
from PIL import Image
from .faceswap import faceswap
import numpy as np

from django.core.files.uploadedfile import InMemoryUploadedFile


def do_faceswap(image, background):
    result = faceswap(image, background)
    result = result.astype(np.uint8)
    pil_img = Image.fromarray(result)
    output_buffer = BytesIO()
    pil_img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)

    binary_data = base64.b64decode(base64_str)
    img_data = BytesIO(binary_data)
    img_data.write(binary_data)
    date_name = date.today()

    img_file = InMemoryUploadedFile(
        file=img_data,
        field_name=None,
        name=str(date_name) + "-" + str(image),
        content_type=image.content_type,
        size=image.size,
        charset=None
    )

    return base64_str, img_file


# def do_faceswaps(images, background, count_of_persons):
#     base64_str = ""
#     img_file = 0
#     faces, coordinates = detect_faces(background, count_of_persons)
#     path_to_backgrounds = r"/app/api/backgrounds/" + "" + background
#     print(path_to_backgrounds)
#     background_pil = Image.open(path_to_backgrounds)
#     for i in range(count_of_persons):
#         image = images[i]
#         background = faces[i]
#         try:
#             result = faceswap(image, background)
#         except NoFaces:
#             continue
#         else:
#             result = faceswap(image, background)
#             list_result = result.astype(np.uint8)
#             pil_result = Image.fromarray(list_result)
#             output_buffer_result = BytesIO()
#             pil_result.save(output_buffer_result, format='JPEG')
#             pil_res = Image.open(output_buffer_result)
#             first_coords = []
#             for i in range(0, 2):
#                 first_coords.append(coordinates[i])
#                 print(first_coords)
#             del coordinates[0:4]
#             first_coords = tuple(first_coords)
#             background_pil.paste(pil_res, box=first_coords)
#             temp = list(first_coords)
#             temp.clear()
#             # background_pil.show()
#             output_buffer = BytesIO()
#             background_pil.save(output_buffer, format='JPEG')
#             byte_data = output_buffer.getvalue()
#             base64_str = base64.b64encode(byte_data)
#
#             binary_data = base64.b64decode(base64_str)
#             img_data = BytesIO(binary_data)
#             img_data.write(binary_data)
#             date_name = date.today()
#
#             img_file = InMemoryUploadedFile(
#                 file=img_data,
#                 field_name=None,
#                 name=str(date_name) + "-" + str(image),
#                 content_type=image.content_type,
#                 size=image.size,
#                 charset=None
#             )
#     return base64_str, img_file



# def detect_faces(image, count_of_persons):
#     print("image", image)
#     path_to_backgrounds = r"/app/api/backgrounds/"
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     image = path_to_backgrounds + image
#     img = cv2.imread(image, cv2.IMREAD_COLOR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     if count_of_persons == 2:
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=2.12, minNeighbors=2, minSize=(180, 180))
#     elif count_of_persons == 3:
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(180, 180))
#     elif count_of_persons == 4:
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(180, 180))
#     if count_of_persons == 5:
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.0999, minNeighbors=5, minSize=(180, 180))
#     image_number = 1
#     face_list = []
#     positions = dict()
#     coordinates = []
#     for (x, y, w, h) in faces:
#         # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#
#         crop = img[y:y + h, x:x + w]
#         coordinates.append(x)
#         coordinates.append(y)
#         coordinates.append(w)
#         coordinates.append(h)
#
#         positions["image"] = x
#         positions["y"] = y
#         positions["w"] = w
#         positions["h"] = h
#         image_number += 1
#         rgb_img = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
#         pil_img = Image.fromarray(rgb_img)
#         face_list.append(pil_img)
#     return face_list, coordinates
