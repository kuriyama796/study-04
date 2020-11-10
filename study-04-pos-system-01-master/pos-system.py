import csv
import datetime

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_master=item_master

    def order_register(self, order):
        for i in self.item_master:
            order_code = input("購入する商品コードを入力してください(終了する場合は' q 'をおしてください): ")
            # q を押したらオーダー登録を終了して会計
            if order_code == 'q':
                break
            # 商品コードがなかったらやり直し
            elif not order.check_item_code(order_code):
                print("商品コード{}はありません".format(order_code))
                continue
            order_count = input("購入する個数を入力してください: ")
            if order_count.isnumeric():
                order.add_item_order(order_code, order_count)
            else:
                print("数字を入力してください")
    
    def add_item_order(self,item_code, item_count):
        order = [item_code, item_count]
        self.item_order_list.append(order)

    def check_item_code(self, item_code):
        for s_item in self.item_master:
            if item_code == s_item.item_code:
                return True
        return False
        
    def view_item_list(self):
        total_price = 0
        # 現在時刻の取得
        now = datetime.datetime.now()
        # テキストファイルのパス
        path = 'receipt/{}.txt'.format(now.strftime('%Y%m%d_%H%M%S'))
        with open(path, mode='w', encoding='utf-8') as f:
            for item in self.item_order_list:
                    for s_item in self.item_master:
                        if item[0] == s_item.item_code:
                            count = item[1]
                            price = (int(count) * int(s_item.price))
                            print("商品コード:{} 商品名:{} 価格:{} 個数:{} 金額:{}".format(s_item.item_code, s_item.item_name, s_item.price, count, str(price)))
                            f.write("商品コード:{} 商品名:{} 価格:{} 個数:{} 金額:{}".format(s_item.item_code, s_item.item_name, s_item.price, count, str(price)) + '\n')
                            total_price += price
            print("合計金額は{}円です".format(total_price))
            f.write("合計金額:{}円".format(total_price) + '\n')
            money = int(input("お預かり金額を金額を入力してください: "))
            f.write("お預かり金額:{}円".format(money) + '\n')
            if money >= total_price:
                print("おつり{}円".format(money - total_price))
                f.write("おつり{}円".format(money - total_price) + '\n')
            else:
                print("お金が足りません")
    
### メイン処理
def main():
    # マスタ登録
    item_master=[]
    with open('source.csv', 'r', encoding="utf-8_sig") as f:
        reader = csv.reader(f)
        for line in reader:
            item_master.append(Item(line[0], line[1], line[2]))
    
    # オーダー登録
    order=Order(item_master)
    order.order_register(order)
    # オーダー表示
    order.view_item_list()
    
if __name__ == "__main__":
    main()