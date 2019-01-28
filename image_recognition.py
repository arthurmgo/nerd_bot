from imageai.Prediction import ImagePrediction
import os
import threading
execution_path = os.getcwd()


prediction = ImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath(os.path.join(execution_path, "model\\resnet50_weights_tf_dim_ordering_tf_kernels.h5"))


class PredictionThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self.result = ""

    def init(self):
        threading.Thread.init(self)

    def run(self):
        prediction.loadModel()
        predictions, percentage_probabilities = prediction.predictImage("image.jpeg", result_count=1)
        for predictions, percentage_probability in zip(predictions, percentage_probabilities):
            self.result = str(predictions + ": " + str(percentage_probability) + "%")
