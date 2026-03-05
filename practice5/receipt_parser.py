import re
import json

def parse_receipt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    items = []
    i = 0

    while i < len(lines):
        line = lines[i]

    
        if re.match(r"^\d+\.$", line):
            i += 1
            product_lines = []

            
            while i < len(lines) and not re.search(r"x \d+(?: \d{3})?,\d{2}", lines[i]):
               
                if not re.match(r"(Стоимость|ИТОГО|Банковская карта|Время|Фискальный|ФП|ИНК|ЗНМ)", lines[i], re.I):
                    product_lines.append(lines[i])
                i += 1

            
            if i < len(lines):
                quantity_price_line = lines[i]
                
                price_match = re.search(r"x \d+(?: \d{3})?,(\d{2})$", quantity_price_line.replace(" ", ""))
                if price_match:
                    
                    price_str = re.search(r"\d+(?: \d{3})?,\d{2}", quantity_price_line.replace(" ", "")).group()
                    price = float(price_str.replace(" ", "").replace(",", "."))
                    
                    name = " ".join(product_lines)
                    items.append({"name": name, "price": price})
                i += 1
        else:
            i += 1

 
    text = "\n".join(lines)
    date_match = re.search(r"(\d{2}\.\d{2}\.\d{4})", text)
    time_match = re.search(r"(\d{2}:\d{2}:\d{2})", text)
    payment_match = re.search(r"(Банковская карта|НАЛ|CASH|CARD|VISA|MASTERCARD)", text, re.I)

    date = date_match.group(1) if date_match else None
    time = time_match.group(1) if time_match else None
    payment_method = payment_match.group().upper() if payment_match else None

    total_amount = sum(item["price"] for item in items)

    result = {
        "date": date,
        "time": time,
        "payment_method": payment_method,
        "total": total_amount,
        "items": items
    }

    return result

if __name__ == "__main__":
    file_path = r"C:\Users\sabin\OneDrive\Pictures\Documents\pp2_2026\practice5\raw.txt"
    parsed = parse_receipt(file_path)
    print(json.dumps(parsed, indent=4, ensure_ascii=False))