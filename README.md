# Image Dataset Builder
This package allows you to create a dataset using your webcam.

## Installation
```
pip install ImgDatasetBuilder
```

## usage
```
from DatasetBuilder import DatasetBuilder

dbuilder = DatasetBuilder(classes=["my_class_one", "my_class_two"], out_dir="./data")

dbuilder.build()
```

You can also pass arguments to the 'build()':

        :param nb_item: - tuple representing  ==> (number_train_data, number_test_data, number_val_data)
                        - you can specify that you don't want a specific dataset by placing -1 at the correct position
                        - DEFAULT : (300, 100, 50)

        :param image_width: webcam's window screen width (DEFAULT = 800)
        :param image_height: webcam's window screen heigh (DEFAULT = 600)
        
