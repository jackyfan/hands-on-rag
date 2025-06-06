from multiprocessing.managers import BaseManager


def test_query_index():
    print('监听5602')
    manager = BaseManager(('127.0.0.1', 5602), b'password')
    manager.register('query_index')
    manager.connect()
    print('发送请求')
    response = manager.query_index('你好！')._getvalue()
    print('resp:{}',response)


if __name__ == "__main__":
    test_query_index()
