import time

from Tools.QrcodeMaker import QrcodeMaker


if __name__ == "__main__":
    time_start = time.time()

    data = """[Q100000023_1&42]{"method":"post","data":{"item2":"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.","item1":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi"""

    qm = QrcodeMaker()
    for i in range(1000):
        qm.make(data, f'./img/{i}.jpg')
        qm.clear()
        if i % 100 == 0:
            print(f"[{i}]: 处理时间: {time.time() - time_start}s")

    time_end = time.time()
    print(time_end - time_start)

