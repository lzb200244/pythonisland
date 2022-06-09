import asyncio
from Movie类 import Movie, timer
from GetData类 import GetData


class Test(Movie, GetData):
    def __init__(self):
        Movie().__init__()

    @timer
    def method(self, ):
        asyncio.get_event_loop().run_until_complete(self.task())
        # asyncio.run(self.task())
        print("爬取完成!")
        # time.sleep(5)
        print("开始存储...")
        self.save_data()
        print("存储完成!")
        self.handle_data()


if __name__ == '__main__':
    obj = Test()
    obj.method()
