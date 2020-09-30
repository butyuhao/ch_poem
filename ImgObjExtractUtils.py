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
        season = {}
        daytime = {}
        weather = {}

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
            if k in ['春季', '春天']:
                season[v] = 1
            elif k in ['夏季', '夏天']:
                season[v] = 2
            elif k in ['秋季', '秋天']:
                season[v] = 3
            elif k in ['冬季', '冬天']:
                season[v] = 4

            # 判断一天中的时间
            if k == '黎明':
                daytime[v] = 1
            elif k in ['黄昏', '日落']:
                daytime[v] = 2
            elif k == '夜晚':
                daytime[v] = 3

            # 判断天气
            if k in ['雨', '暴雨']:
                weather[v] = 1
            elif k in ['雪']:
                weather[v] = 2
            elif k in ['雾', '薄雾']:
                weather[v] = 2


        # 取排序后的最有可能的结果 season
        sorted(season.items(), key=lambda x: x[0], reverse=True)
        season_result = 0
        for s_v in season.values():
            season_result = s_v
            break;

        # 取排序后的最有可能的结果 daytime
        sorted(daytime.items(), key=lambda x:x[0], reverse=True)
        daytime_result = 0
        for d_v in daytime.values():
            daytime_result = d_v
            break;

        # 取排序后的最有可能的结果 weather
        sorted(weather.items(), key=lambda x: x[0], reverse=True)
        weather_result = 0
        for w_v in weather.values():
            weather_result = w_v
            break;

        return result_dict, obj_dict, season_result, daytime_result, weather_result


if __name__ == '__main__':
    # 指定图片路径
    img_path = r'./data/test4.jpg'
    # 创建提取器对象
    extractor = ImgObjExtractor()
    # 调用并获取结果
    ori_dict, obj_dict, season_num, daytime, weather = extractor.extract_single_img(img_path)
    # 原始的提取结果
    print('ori_dict', ori_dict)
    # 提取结果中的名词(物体)
    print('obj_dict', obj_dict)
    # season 0:未知 1:春 2:夏 3:秋 4:冬
    print('season:', season_num)
    # daytime 0:未知 1:黎明 2:傍晚 3:夜晚
    print('daytime', daytime)
    # weather 0:未知 1:雨 2:雪 3:雾
    print('weather', weather)
