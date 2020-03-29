import cv2
import time
import copy
import os
import sys


class DatasetBuilder:
    def __init__(self, classes, out_dir):
        """
        :param classes: classes of the dataset that we'll create
        :param out_dir: directory where we'll store the freshly created datased
        """
        self.classes = classes
        self.out_dir = out_dir

    def __build_folder_structure(self, nb_item):
        """
        :param nb_item: - tuple representing  ==> (number_train_data, number_test_data, number_val_data)
                        - you can specify that you don't want a specific dataset by placing -1 at the correct position
        """
        print("Building the folder structures : ")
        if os.path.exists(self.out_dir):
            sys.exit('The out_dir that you specified already exists')
        print(self.out_dir)
        os.makedirs(self.out_dir)

        for i in range(len(nb_item)):
            if nb_item[i] != -1:
                dataset_name = "Train" if i == 0 else "Test" if i == 1 else "Val"
                dataset_dir = os.path.join(self.out_dir, dataset_name)
                os.makedirs(dataset_dir)
                print("  --> {}".format(dataset_name))
                for c in self.classes:
                    print("    - {}".format(c))
                    current_dir = os.path.join(dataset_dir, c)
                    os.makedirs(current_dir)

    def build(self, nb_item=(300, 100, 50), image_width=800, image_height=600):
        """
        :param nb_item: - tuple representing  ==> (number_train_data, number_test_data, number_val_data)
                        - you can specify that you don't want a specific dataset by placing -1 at the correct position
                        - default : (300, 100, 50)

        :param image_width: webcam's window screen width (DEFAULT = 800)
        :param image_height: webcam's window screen heigh (DEFAULT = 600)
        """
        self.__build_folder_structure(nb_item)

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, image_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, image_height)

        class_position = 0
        item_position = 0

        start_capture = False
        start_time = 0
        timer = 5

        nb_current_class = 0

        while class_position < len(self.classes):
            # Capture frame-by-frame
            ret, frame = cap.read()
            clean_frame = copy.deepcopy(frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                start_capture = True
                start_time = time.time()

            if not start_capture:
                text = "Class : "+ self.classes[class_position] + " (Press 's' to start recording)"
                cv2.putText(frame, text, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255),
                            thickness=2)
            else:
                if nb_item[item_position] != -1:  # if the current item will be recorded
                    seconds_left = int(timer - (time.time() - start_time))
                    if seconds_left <= 0:
                        dataset_name = ("Train" if item_position == 0 else "Test" if item_position == 1 else "Val")
                        text = "{} captures taken for {} [{}]".format(nb_current_class, self.classes[class_position],
                                                                      dataset_name)
                        cv2.putText(frame, text, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255),
                                    thickness=2)

                        filename = "{}_{}.jpg".format(self.classes[class_position], nb_current_class)
                        file_path = os.path.join(self.out_dir, dataset_name, self.classes[class_position], filename)
                        cv2.imwrite(file_path, clean_frame)

                        nb_current_class += 1
                    else:
                        text = "Capture for class {} starts in {} seconds".format(self.classes[class_position],
                                                                                  seconds_left)
                        cv2.putText(frame, text, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255),
                                    thickness=2)

            # if finished downloading items or the user doesn't want to save the test/val set
            if nb_current_class == nb_item[item_position] or nb_item[item_position] == -1:
                item_position += 1
                nb_current_class = 0

            if item_position == 3:  # finished capturing images for a class
                item_position = 0
                class_position += 1
                start_capture = False

            # Display the resulting frame
            cv2.imshow('Webcam', frame)

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        print("Finished creating dataset !")
