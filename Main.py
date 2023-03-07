import matplotlib.pylab as plt
from API import transfer_style
import os
from PIL import Image

if __name__=="__main__":

    # Empty the log file
    open("./log.txt", 'w').close()

    # Path of the pre-trained TF model 
    model_directory_path = "./model"

    # Old code, suited for one image at a time
    # # NOTE : Works only for '.jpg' and '.png' extensions,other formats may give error
    # content_image_path = r"./Input_Images/+_cd0adc4e2d3f4fc9329304f86ff6131a.jpg"
    # style_image_path = r"./Input_Styles/s1.jpg"
    #
    # img = transfer_style(content_image_path,style_image_path,model_directory_path)
    # # Saving the generated image
    # plt.imsave('./Output/output_image.jpeg',img)

    input_file_directory_path = "./Input_Images"
    input_style_directory_path = "./Input_Styles"


    # Check style inputs for RGB format before starting the batch run
    for input_style_path in os.listdir(input_style_directory_path):
        # print(plt.imread(input_style_directory_path + "/" + input_style_path).shape)
        if (plt.imread(input_style_directory_path + "/" + input_style_path).shape[2] == 4):
            img = Image.open(input_style_directory_path + "/" + input_style_path)
            img.load()
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            new_filename = os.path.splitext(input_style_path)[0] + "_RGB.jpg"
            background.save(input_style_directory_path + "/" + new_filename, "JPEG", quality=90)
            os.remove(input_style_directory_path + "/" + input_style_path)

    for input_file_path in os.listdir(input_file_directory_path):
        flag_is_rgb = True
        flag_is_original_size = True
        height, width, depth = plt.imread(input_file_directory_path+"/"+input_file_path).shape

        # Test if the image is in RGB format and not RGBA, which would have a depth of 4
        if (depth == 4):
            # https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil
            flag_is_rgb = False
            img = Image.open(input_file_directory_path+"/"+input_file_path)
            img.load()
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            new_filename = "RGB_"+os.path.splitext(input_file_path)[0]+".jpg"
            background.save(input_file_directory_path+"/"+new_filename, "JPEG", quality=90)
            with open("./log.txt", "a") as myfile:
                myfile.write("Converted file "+input_file_path+" to RGB")
            # Use converted image in following steps
            input_file_path = new_filename

        # Downscale images which will blow up my memory usage
        if (height > 3000 or width > 3000):
            flag_is_original_size = False
            img = Image.open(input_file_directory_path+"/"+input_file_path)
            size = width/2, height/2
            new_filename = "SMALLER_"+ os.path.splitext(input_file_path)[0]+".jpg"
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(input_file_directory_path+"/"+new_filename, "JPEG")
            # Delete previously created temporary file
            if (flag_is_rgb == False):
                os.remove(input_file_directory_path + "/" + input_file_path)
            # Use rescaled image in following steps
            input_file_path = new_filename

        abbreviated_filename = input_file_path[:50]
        if not os.path.exists("./Output/" + abbreviated_filename):
            # if the demo_folder directory is not present
            # then create it.
            os.makedirs("./Output/" + abbreviated_filename)
        for input_style_path in os.listdir(input_style_directory_path):
            img = transfer_style(input_file_directory_path+"/"+input_file_path,
                                 input_style_directory_path + "/" + input_style_path,
                                 model_directory_path)
            plt.imsave('./Output/' + abbreviated_filename + "/" + abbreviated_filename + "_" + input_style_path + ".jpeg",img)
        if (flag_is_rgb == False or flag_is_original_size == False):
            # Remove converted temporary image
            os.remove(input_file_directory_path+"/"+input_file_path)





