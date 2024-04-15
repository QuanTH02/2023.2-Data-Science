text = "Eiga Doraemon: Nobita to Sora no Utopia (映画ドラえもん のび太と空の理想郷（ユートピア）) (2023)"
# Tách chuỗi bằng dấu ngoặc đơn '(' và lấy phần tử cuối cùng
year = text.split('(')[-1].strip(')')

a = text.split(' (')[0]

print(a)
