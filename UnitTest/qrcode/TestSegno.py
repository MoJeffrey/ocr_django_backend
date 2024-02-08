import time

import segno


def generate_qr_code(data, filename):
    # 创建 QR 码对象
    qr = segno.make(data)

    # 保存 QR 码为图片文件
    qr.save(filename)


if __name__ == "__main__":
    time_start = time.time()

    data = """[Q100000023_1&42]{"method":"post","data":{"item2":"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.","item1":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi"""

    for i in range(1000):
        generate_qr_code(data, f'./img/{i}.png')
        if i % 100 == 0:
            print(f"[{i}]: 处理时间: {time.time() - time_start}s")

    time_end = time.time()
    print(time_end - time_start)