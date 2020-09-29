from clarifai.rest import ClarifaiApp

class imgObjExtractor:
    def __init__(self):
        app = ClarifaiApp(api_key='11ac3a53e15a435e8f66f1f034824403')
        self.model = app.public_models.general_model
    def extract_single_img(self, img_path):
        response = self.model.predict_by_filename(img_path)
        response_list = response['outputs'][0]['data']['concepts']

        result_dict = {}
        for result in response_list:
            result_dict[result['name']] = result['value']
        return result_dict

if __name__ == '__main__':
    img_path = r'C:\Users\butyu\Desktop\test.jpg'
    extractor = imgObjExtractor()
    result = extractor.extract_single_img(img_path)
    print(result)


