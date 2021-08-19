import os
import scripts

folder = input("Enter the name of folder(dataset name) : ")

#Make Output Directories
scripts.make_directories()

#Copy files from input to JPEGImages in output
scripts.copy_jpg_files("input","output/JPEGImages")

# Converts to jetson-inference xml format
for filename in os.listdir("input"):
    print("Converting " + filename)
    if filename.endswith(".xml"):
        scripts.convert_to_jetson_xml(filename, folder)
        print(filename+" converted successfully")


# Write ImageSets text files (i.e. trainval train val test)
scripts.write_image_sets_data()