import cv2
import os


image_dict = {}


def check_folder(directory: str):
    for filename in os.listdir(directory):
        if "." not in filename:  # if a folder
            check_folder(directory + "//" + filename)
        else:  # if it isn't a folder
            if ".png" in filename:
                img = cv2.imread(directory + "//" + filename)
                image_dict[filename] = (img.shape[0], img.shape[1])


if __name__ == "__main__":
    directory = "C:\MyFiles\Python Related Files\TSA\TSA-Software-App-2020-\ActualApp\Wireframe\Image"
    check_folder(directory)
    print(image_dict)