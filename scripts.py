import math
import xml.etree.ElementTree as ET
import os
import shutil

#Make directories
def make_directories():
    #Removes all existing file
    for filenames in os.listdir("output"):
        os.remove("output/"+filenames)

    #Make the new directories
    os.makedirs("output/Annotations")
    os.makedirs("output/JPEGImages")
    os.makedirs("output/ImageSets/Main")

#Takes xml file and convert it to xml for jetson-inference library
def convert_to_jetson_xml(xml_file,folder):
    tree = ET.parse("input/"+xml_file)
    root = tree.getroot()

    # Changes in <folder> element
    # Removes <folder> element for replacing
    for elm in root.findall("./folder"):
        root.remove(elm)
    # Creates new <folder> element and add into appropriate position
    folder_element = ET.Element("folder")
    folder_element.text = folder
    folder_element.tail = "\n    "  # This line formats the element to be properly aligned with one level of indentation
    root.insert(1, folder_element)

    # Changes in <source> element
    # removes <database> element
    for elm in root.findall("./source/database"):
        root[3].remove(elm)  # root[3] is <source>, removes <database> element
    # Create and add <database>, <annotation> and <image> to <source> element
    for elm in root.findall("./source"):
        database_element = ET.Element("database")
        database_element.text = folder
        database_element.tail = "\n        "
        annotation_element = ET.Element("annotation")
        annotation_element.text = "custom"
        annotation_element.tail = "\n        "
        image_element = ET.Element("image")
        image_element.text = "custom"
        image_element.tail = "\n    "
        elm.insert(0, database_element)
        elm.insert(1, annotation_element)
        elm.insert(2, image_element)

    # Changes in <path> element
    # Removes <path> element
    for elm in root.findall("./path"):
        root.remove(elm)

    # Write xml file with same name as img file
    for elm in root.findall("./filename"):
        img_file = elm.text[:-4]  # Removes file extension (Only works with 3 letters extensions)
    tree.write("output/Annotations/"+img_file + ".xml")

#copy all jpg files over to another dir
def copy_jpg_files(input_dir,output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg"):
            shutil.copy2(input_dir+"/"+filename,output_dir)


#count number of jpg files in directory
def count_jpg_in_dir(dir):
    jpg_count=0
    for filename in os.listdir(dir):
        if filename.endswith(".jpg"):
            jpg_count+=1

    print("Total JPG Files Found: "+str(jpg_count))
    return jpg_count

#Split data into trainval(90%) train(80%) val(10%) test(10%)
#writes into text file under ImageSets
def write_image_sets_data():
    total_number_of_files = count_jpg_in_dir("output/JPEGImages")

    #Clear content of files
    open('output/ImageSets/Main/trainval.txt', 'w').close()
    open('output/ImageSets/Main/train.txt', 'w').close()
    open('output/ImageSets/Main/val.txt', 'w').close()
    open('output/ImageSets/Main/test.txt', 'w').close()

    train_count = math.floor(0.8*total_number_of_files)
    val_count = math.floor(0.1*total_number_of_files)
    trainval_count = train_count+val_count
    test_count = math.floor(0.1*total_number_of_files)

    files = os.listdir("output/JPEGImages")
    for i in range(0,len(files)):
        files[i] = files[i][:-4]

    for i in range(0,trainval_count):
        f=open('output/ImageSets/Main/trainval.txt', 'a')
        f.write(files[i])
        if(i!=trainval_count-1):
            f.write("\n")
        f.close()

    for i in range(0,train_count):
        f = open('output/ImageSets/Main/train.txt', 'a')
        f.write(files[i])
        if (i != train_count-1):
            f.write("\n")
        f.close()

    for i in range(train_count,train_count+val_count):
        f = open('output/ImageSets/Main/val.txt', 'a')
        f.write(files[i])
        if (i != train_count+val_count-1):
            f.write("\n")
        f.close()

    for i in range(train_count+val_count,len(files)):
        f = open('output/ImageSets/Main/test.txt', 'a')
        f.write(files[i])
        if (i != len(files)-1):
            f.write("\n")
        f.close()


