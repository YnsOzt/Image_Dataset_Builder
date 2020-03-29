from src.DatasetBuilder import DatasetBuilder

dbuilder = DatasetBuilder(classes=["one", "three"], out_dir="./data")

dbuilder.build(nb_item=(10, -1, 10))
