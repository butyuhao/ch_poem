from clarifai.rest import ClarifaiApp
import jieba.posseg as psg


class ImgObjExtractor:
    def __init__(self):
        app = ClarifaiApp(api_key='11ac3a53e15a435e8f66f1f034824403')
        self.model = app.public_models.general_model

    def extract_single_img(self, img_path):
        response = self.model.predict_by_filename(img_path)
        response_list = response['outputs'][0]['data']['concepts']

        result_dict = {}
        obj_dict = {}
        season = 0
        daytime = {}

        print(result_dict)

        for r in response_list:
            result_dict[r['name']] = r['value']
        for k, v in result_dict.items():
            # 提取出结果中的名词
            noun_flag = True
            for x in psg.cut(k):
                if x.flag != 'n' and x.flag != 'nr':
                    noun_flag = False
            if noun_flag:
                obj_dict[k] = v
            # 判断结果所在季节
            if k == '春季' or k == '春天':
                season = 1
            elif k == '夏季' or k == '夏天':
                season = 2
            elif k == '秋季' or k == '秋天':
                season = 3
            elif k == '冬季' or k == '冬天':
                season = 4
            # 判断一天中的时间
            if k == '黎明':
                daytime[v] = 1
            elif k in ['黄昏', '日落']:
                daytime[v] = 2
            elif k == '夜晚':
                daytime[v] = 3
            sorted(daytime.items(), key=lambda x:x[0], reverse=True)

            # 取排序后的最有可能的结果
            daytime_result = 0
            for d_v in daytime.values():
                daytime_result = d_v
                break;

        return obj_dict, season, daytime_result


if __name__ == '__main__':
    img_path = r'C:\Users\butyu\Desktop\test1.jpg'
    extractor = ImgObjExtractor()
    obj_dict, season_num, daytime = extractor.extract_single_img(img_path)
    print(obj_dict)
    print(season_num)
    # daytime 0:未知 1:黎明 2:傍晚 3:夜晚
    print(daytime)
