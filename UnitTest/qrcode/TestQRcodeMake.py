import os
import time

import jpype

from Tools.QrcodeMaker import QrcodeMaker

if __name__ == "__main__":
    QrcodeMaker.Init('../../javaTools/')

    data = """[Q100000023_1&42]{"method":"post","data":{"item2":"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.","item1":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi"""

    data_list = []
    fileName_list = []

    for i in range(100):
        data_list.append(data)
        fileName_list.append(str(i))

    time_start = time.time()
    b = QrcodeMaker.make(data_list, fileName_list, f'{os.getcwd()}/img/')

    time_end = time.time()
    print(time_end - time_start)
    print(b)
    print(type(b))
