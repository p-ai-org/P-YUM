import cv2
import os
import urllib.request

# create "Thumbnail Photos" folder if it doesn't exist
if not os.path.exists("Thumbnail Photos"):
    os.makedirs("Thumbnail Photos")

# list of youtube video links
links = ["https://www.youtube.com/watch?v=ahxKAlbp6DU",
         "https://www.youtube.com/watch?v=uYIDfBbgVVI"]

# scrape and save thumbnails
for link in links:
    # get video id from link
    video_id = link.split("?v=")[1]

    # thumbnail url
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

    # save thumbnail
    urllib.request.urlretrieve(
        thumbnail_url, f"Thumbnail Photos/{video_id}.jpg")


# open "Thumbnail Photos" folder
folder = "Thumbnail Photos"
if not os.path.exists(folder):
    print(f"Error: {folder} does not exist")
    exit()

####################################


# Check if the file "thumbnail.csv" exists
if os.path.exists("thumbnail.csv"):

    # If it exists, check if it has content
    if os.path.getsize("thumbnail.csv") > 0:

        # If it has content, delete the content
        # Keep the header row
        with open("thumbnail.csv", "w") as csv_file:
            csv_file.write("filename,face detected?\n")

else:
    # If it doesn't exist, create it and write a header row
    with open("thumbnail.csv", "w") as csv_file:
        csv_file.write("filename,face detected?\n")


# load face detector
face_detector = cv2.CascadeClassifier(os.path.join(
    "Scripts", "haarcascade_frontalface_default_new.xml"))

# loop through JPG files in folder
for filename in os.listdir(folder):
    if filename.endswith(".jpg"):
        print(filename)
        # read image
        img = cv2.imread(os.path.join(folder, filename))

        # convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # detect faces
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # draw rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # show image
        cv2.imshow(filename, img)

        # if there are faces, return that a face was detected
        if len(faces) > 0:
            with open("thumbnail.csv", "a") as csv_file:
                csv_file.write(f"{filename},yes\n")
            
            cv2.imwrite(f"Thumbnail Photos/{filename}", img)
        else:
            # if there were no faces, return that a face wasn't detected
            with open("thumbnail.csv", "a") as csv_file:
                csv_file.write(f"{filename},no\n")

# wait for user to press any key
cv2.waitKey(0)

# destroy all windows
cv2.destroyAllWindows()
