import bz2

def compress_string(string):
    return bz2.compress(string.encode())

def decompress_string(compressed_data):
    return bz2.decompress(compressed_data).decode()

original_string = "Your original string"
compressed_data = compress_string(original_string)
print("Compressed data:", compressed_data)

decompressed_string = decompress_string(compressed_data)
print("Decompressed string:", decompressed_string)
