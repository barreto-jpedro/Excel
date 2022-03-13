import json

 
def read_database(path: str) -> dict:
    try:
        with open(path, "r") as json_file:
            json_object = json.load(json_file)
            json_file.close()
            return json_object
    except FileNotFoundError:
        print('ERRO: arquivo não encontrado')
        return {}
    except Exception as err:
        print('Ocorreu um erro desconhecido. Segue o erro:\n', err)
        return {}


def build_bills_list(database: dict):
    bills_builded = list()
    new_item = dict()
    for bill in database.get('bill', []):
        items = bill.get('items', [])
        for item in items:
            new_item['id'] = item.get('id', '')
            product = get_product_by_id(database, new_item['id'])
            new_item['name'] = product.get('name', None)
            new_item['quantity'] = item.get('quantity', None)
            if product.get('weight', False):
                new_item['weight'] = 'False'
                new_item['total_price'] = item.get(
                    'quantity', 0) / product.get('measure_quantity', 0) * product.get('unit_price', 0)
                new_item['quantity'] = str(
                    new_item['quantity']) + ' ' + product.get('measure', 0)
            else:                
                new_item['total_price'] = item.get(
                    'quantity', 0) * product.get('unit_price', 0)
                new_item['quantity'] = str(
                    new_item['quantity']) + ' unidade(s)'

            new_item['weight'] = product.get('weight', 'False')
            new_item['unit_price'] = product.get('unit_price', 0)
            new_item['measure'] = product.get('measure', 'none')
            new_item['total_price'] = round(new_item['total_price'], 2)
            bills_builded.append(new_item.copy())
    return bills_builded


def get_product_by_id(database: dict, id: int):
    for product in database.get('products', []):
        if product['id'] == id:
            return product
    else:
        return {}


def show_bill(path: str):
    database = read_database(path)
    bills = build_bills_list(database)
    if bills:
        total = 0
        for bill in bills:
            print('{:<70}'.format(bill.get('name', '')), end='')
            print('{:^20}'.format(bill.get('quantity', 0)), end='')
            print('{:>20}'.format(bill.get('total_price', 0)))
            total += bill.get('total_price', 0)
        print('-'*110)
        print('{:<80}{:>30}'.format('TOTAL', round(total, 2)))
        print('\n\nTotal de produtos verificados: ', len(bills))
    else:
        print('Não existem notas!')
