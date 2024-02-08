from zxing import BarCodeWriter, Color, ImageWriter

img = cv2.imread("test.jpg")
det = cv2.QRCodeDetector()
val, pts, st_code = det.detectAndDecode(img)
print(val)

if __name__ == "__main__":
    time_start = time.time()

    data = """[Q100000023_1&42]{"method":"post","data":{"item2":"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.","item1":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi"""

    qm =  zxing.BarCodeReader()
    for i in range(1000):
        barcode = reader.decode(data)
        barcode
        qm.make(data, f'./img/{i}.jpg')
        qm.clear()
        if i % 100 == 0:
            print(f"[{i}]: 处理时间: {time.time() - time_start}s")

    time_end = time.time()
    print(time_end - time_start)

