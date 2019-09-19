import fastai
import fastai.vision
import fastai.metrics
import fastai.basic_train

import torch

import pathlib


class Recognizer:
    def get_confidence(self, prediction, categories, thresh: float = 0.0):
        '''
        show the confidence that recognized image is each category
        
        Parameters:
        prediction: input tuple(fastai.core.Category, torch.Tensor, torch.Tensor )
        
            only the last element of the tuple is used, assumed to be an array of probablities for category membership
        
        categories: input 
        
            list of strings, being category names
            
        name: input str
        
            name of image being processed
            
        thresh: input float
            probablities smaller than this are not reported; by default, all are reported
        
        Returns: list of tuples (str, str) being (category name ,probablity), reverse sorted on probability 
        '''

        #  range over all categories: 
        #  if a category has a prob greater than the threshhold, add a tuple to the 
        #   guesses list (name, prob)
        guesses = [
            (categories[i],
            '{:5.3f}'.format(prediction[2][i].item())  )
            for i in range(len(categories))
            if (prediction[2][i].item() > thresh)
        ]

        # sort the guesses in descending order of likelihood
        sg = sorted(guesses, key=lambda x: x[1], reverse=True)

        return sg

    # end show_confidence

    def recognize(self, model_path: str, image_path: str):

        learn2 = fastai.basic_train.load_learner(model_path)

        fastai.torch_core.defaults.device = torch.device('cpu')

        img_test2 = fastai.vision.open_image(image_path).resize(200)
        prediction2 = learn2.predict(img_test2)

        sorted_guesses = self.get_confidence(prediction2, learn2.data.classes, 0.0005)

        return sorted_guesses

    # end recognize


# end Recognizer

