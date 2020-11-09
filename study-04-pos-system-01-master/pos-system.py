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
    
    def add_item_order(self,item_code, item_count, money):
        # 商品コードの確認
        for i in range(len(self.item_master)):
            if item_code == self.item_master[i].item_code:
                self.price = int(self.item_master[i].price)
                self.money = int(money)
                # 残金を計算
                self.money -= self.price * int(item_count)
                # 残金が1円以上ならオーダー登録
                if self.money > 0:
                    order = [item_code, item_count]
                    self.item_order_list.append(order)
                    print("残金:{}".format(self.money))
                    return self.money
                    #残高が0円ならオーダー登録して終了
                elif self.money == 0:
                    order = [item_code, item_count]
                    self.item_order_list.append(order)
                    print("残金がなくなったので終了します")
                    return True
                else:
                    print("残金が足りません")
                    return False
        print("商品コード{}は存在しません".format(item_code))
        
    def view_item_list(self, money):
        # 現在時刻の取得
        now = datetime.datetime.now()
        # テキストファイルのパス
        path = 'receipt/{}.txt'.format(now.strftime('%Y%m%d_%H%M%S'))
        with open(path, mode='w', encoding='utf-8') as f:
            for item in self.item_order_list:
                for s_item in self.item_master:
                    if item[0] == s_item.item_code:
                        count = item[1]
                        total_price = (int(count) * int(s_item.price))
                        print("商品コード:{} 商品名:{} 価格:{} 個数:{} 合計金額:{}".format(s_item.item_code, s_item.item_name, s_item.price, count, str(total_price)))
                        f.write("商品コード:{} 商品名:{} 価格:{} 個数:{} 合計金額:{}".format(s_item.item_code, s_item.item_name, s_item.price, count, str(total_price)) + '\n')
            print("おつり:{}".format(money))
            f.write("おつり:{}".format(money))
    
### メイン処理
def main():
    # マスタ登録
    item_master=[]
    with open('source.csv', 'r', encoding="utf-8_sig") as f:
        reader = csv.reader(f)
        for line in reader:
            item_master.append(Item(line[0], line[1], line[2]))


    # item_master.append(Item("001","りんご",100))
    # item_master.append(Item("002","なし",120))
    # item_master.append(Item("003","みかん",150))

    money = input("お預かり金額を入力してください: ")
    
    # # オーダー登録
    order=Order(item_master)

    for i in item_master:
        order_code = input("購入する商品コードを入力してください(終了する場合は' q 'をおしてください): ")
        if order_code == 'q':
            break
        order_count = input("購入する個数を入力してください: ")
        if order_count.isnumeric():
            result = order.add_item_order(order_code, order_count, money)
            if result == True:
                money = 0
                break
            elif result == False:
                continue
            else: 
                money = result
        else:
            print("数字を入力してください")
    # order.add_item_order("001")
    # order.add_item_order("002")
    # order.add_item_order("003")
    
    
    # オーダー表示
    order.view_item_list(money)
    
if __name__ == "__main__":
    main()