#Convert mp4 to gif
#python 3.11
#Author: Aaron Beckley
#7/10/2023
import cv2
import glob
import argparse
from PIL import Image
import os


def main():
    try:
        argParse = argparse.ArgumentParser(description='A simple tool for converting an mp4 file to a gif', prog='mp4 to gif')
        argParse.add_argument('-v', '--version', action='version', version='%(prog)s version 1.1')
        argParse.add_argument('-f', '--file', action='store', type=str, help='The mp4 file you wish to convert to gif')
        argParse.add_argument('-d', '--directoryToGif', action='store', type=str, help='If you have directory of just images (jpegs) use this, and it will convert the directory of images to a gif')
        argParse.add_argument('-l', '--loopCount', action='store', type=str, help='Change the default loop count')
        argParse.add_argument('-m', '--duration', action='store', type=str, help='Change the default duration in ms')
        argParse.add_argument('-q', '--quality', action='store', type=str, help='Change the default quality for the jpegs')
        argParse.add_argument('-s', '--skip', action='store_true', help='Just outputs the frames from the video file, skips creating gif from images.')
        args = argParse.parse_args()
        if args.file and args.directoryToGif:
            print("Needs to either be an mp4 file, or a directory of images")
            exit()
        if args.file == None:
            if args.directoryToGif == None:
                print("Please select a file to convert")
                exit()
            else:
                print("Converting directory of images to gif")
                make_gif(args.directoryToGif, args.duration, args.loopCount)
                exit()
        else:
            print("Converting mp4 file")
            convert_mp4_to_jpgs(args.file, args.quality)
            print("Converting directory of images to gif")
            if not args.skip:
                make_gif(os.path.basename(os.path.splitext(args.file)[0]), args.duration, args.loopCount)
            print("Finished")
            exit()
    except KeyboardInterrupt:
        print(' is caught, exiting...')
        exit()


#https://www.blog.pythonlibrary.org/2021/06/29/converting-mp4-to-animated-gifs-with-python/
def convert_mp4_to_jpgs(path, quality):
    video_capture = cv2.VideoCapture(path)
    still_reading, image = video_capture.read()
    frame_count = 0
    if quality == None:
        quality = 95
    #https://stackoverflow.com/questions/1274405/how-to-create-new-folder
    if not os.path.exists(os.path.basename(os.path.splitext(path)[0])):
        os.makedirs(os.path.basename(os.path.splitext(path)[0]))
    while still_reading:
        #https://stackoverflow.com/questions/58375458/saving-an-image-in-opencv-increase-image-size
        cv2.imwrite(os.path.basename(os.path.splitext(path)[0])+f"/frame_{frame_count:010d}.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        
        # read next image
        still_reading, image = video_capture.read()
        frame_count += 1

#need to make a more memory efficient implementation
def make_gif(frame_folder, durationCount, loopCount):
    images = glob.glob(f"{frame_folder}/*.jpg")
    images.sort()
    frames = [Image.open(image) for image in images]
    #frame_one = frames[0]
    if durationCount == None:
        durationCount = 50
    if loopCount == None:
        loopCount = 0
    #https://stackoverflow.com/questions/33372054/given-a-path-how-can-i-extract-just-the-containing-folder-name
    #https://stackoverflow.com/questions/621354/how-to-slice-a-list-from-an-element-n-to-the-end-in-python
    #https://stackoverflow.com/questions/10607468/how-to-reduce-the-image-file-size-using-pil
    frames[0].save(os.path.basename(frame_folder)+".gif", format="GIF", append_images=frames[1:], #You can set the duration of each frame in milliseconds. In this example, you set it to 100 ms. Finally, you set loop to 0 (zero), which means that you want the GIF to loop forever. If you set it to a number greater than zero, it would loop that many times and then stop. #https://www.blog.pythonlibrary.org/2021/06/23/creating-an-animated-gif-with-python/
                   save_all=True, duration=float(durationCount), loop=int(loopCount))
    

if __name__ == "__main__":
    main()


