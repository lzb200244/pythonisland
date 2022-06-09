import pandas as pd


class GetData:
    data = None

    def read_csv(self):

        data = pd.read_csv("电影分析.csv", encoding="utf8", header=None)
        self.data = data.loc[:, [0, 1, 2]]

    def handle_data(self):
        self.read_csv()
        self.data[3] = self.data[1].map(self.fun)
        self.data[4] = self.data[1].map(self.fun2)
        data = self.data.loc[:, [0, 2, 3, 4]]
        data_1 = data.loc[:, [0, 2, 3]]
        data_2 = data.loc[:, [0, 2, 4]]
        data_2 = data_2.loc[data[4] != "null"]
        data_2 = data_2.rename(columns={4: 3})
        # data = data_1.append(data_2)
        data = pd.concat([data_1, data_2], join="inner", )
        data = data.groupby(3).mean().round(2)
        data.to_csv("data.csv", index_label=0)
        # data = pd.read_csv("data.csv").rename(columns={"0": "类型", "2": "评分"}).to_dict(orient="records")
        data = pd.read_csv("data.csv").rename(columns={"0": "name", "2": "value"})
        return data

    @staticmethod
    def fun(item):
        return item.split('/')[0]

    @staticmethod
    def fun2(item):


        if "/" in item:
            return item.split("/")[1]
        else:
            return "null"


if __name__ == '__main__':
    print("我是GetData类")
