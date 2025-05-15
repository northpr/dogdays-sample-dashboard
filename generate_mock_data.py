import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Define the number of records to generate
num_records = 500

# Define date range (last 6 months)
end_date = datetime.now()
start_date = end_date - timedelta(days=180)
date_range = (end_date - start_date).days

# Define dog food products
products = [
    {"code": "DD001", "name": "Premium Puppy Kibble (Small Breed)", "price": 1200, "category": "Dry Food"},
    {"code": "DD002", "name": "Premium Adult Kibble (All Breeds)", "price": 1500, "category": "Dry Food"},
    {"code": "DD003", "name": "Premium Senior Kibble (Large Breed)", "price": 1600, "category": "Dry Food"},
    {"code": "DD004", "name": "Grain-Free Salmon & Sweet Potato", "price": 1800, "category": "Dry Food"},
    {"code": "DD005", "name": "Weight Management Formula", "price": 1400, "category": "Dry Food"},
    {"code": "DD006", "name": "Sensitive Stomach Formula", "price": 1700, "category": "Dry Food"},
    {"code": "DD007", "name": "Beef & Vegetable Wet Food", "price": 120, "category": "Wet Food"},
    {"code": "DD008", "name": "Chicken & Rice Wet Food", "price": 120, "category": "Wet Food"},
    {"code": "DD009", "name": "Lamb & Pea Wet Food", "price": 130, "category": "Wet Food"},
    {"code": "DD010", "name": "Dental Chew Sticks (Small)", "price": 250, "category": "Treats"},
    {"code": "DD011", "name": "Dental Chew Sticks (Large)", "price": 350, "category": "Treats"},
    {"code": "DD012", "name": "Training Treats (Chicken)", "price": 180, "category": "Treats"},
    {"code": "DD013", "name": "Peanut Butter Biscuits", "price": 200, "category": "Treats"},
    {"code": "DD014", "name": "Hip & Joint Supplement", "price": 800, "category": "Supplements"},
    {"code": "DD015", "name": "Skin & Coat Supplement", "price": 750, "category": "Supplements"},
    {"code": "DD016", "name": "Multivitamin Chews", "price": 600, "category": "Supplements"},
    {"code": "DD017", "name": "Puppy Starter Kit", "price": 2500, "category": "Bundles"},
    {"code": "DD018", "name": "Senior Care Package", "price": 2800, "category": "Bundles"}
]

# Define sales channels
channels = ["Lazada", "Shopee", "Website", "In-store", "Distributor"]
channel_weights = [0.3, 0.25, 0.2, 0.15, 0.1]  # Probability weights

# Define provinces in Thailand
provinces = [
    "Bangkok", "Chiang Mai", "Phuket", "Chonburi", "Khon Kaen", 
    "Songkhla", "Nonthaburi", "Pathum Thani", "Nakhon Ratchasima", 
    "Udon Thani", "Surat Thani", "Chiang Rai", "Rayong", "Ayutthaya"
]
province_weights = [0.25, 0.1, 0.1, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05, 0.04, 0.04, 0.03, 0.03, 0.02]

# Define customer names (fictional)
first_names = [
    "Somchai", "Somsak", "Somying", "Somporn", "Somrak", "Somjai", "Somkiat", "Somkid", 
    "Nattapong", "Nattaporn", "Nattawut", "Nattacha", "Nattaya", "Nattanon", "Nattanicha",
    "Siriwan", "Siriporn", "Siripat", "Sirichai", "Sirirat", "Sirithorn", "Siripong",
    "Wichai", "Wichit", "Wichian", "Wichan", "Wichaya", "Wichuda", "Wichuda",
    "Rattana", "Ratree", "Ratchanee", "Ratchada", "Ratchanok", "Ratchapol", "Ratchaphon"
]
last_names = [
    "Suksawat", "Srisuk", "Saengchan", "Sae-tang", "Sae-lim", "Ruangrit", "Ruangsan",
    "Pongpanich", "Pongsakorn", "Pongsak", "Pongsuwan", "Pongthep", "Pongpat",
    "Nakorn", "Nakornthai", "Nakornthap", "Nakornsri", "Nakornpat", "Nakornpol",
    "Jaidee", "Jaiyen", "Jaipak", "Jaisai", "Jairai", "Jairak", "Jairam",
    "Thongchai", "Thongsuk", "Thongsri", "Thongpai", "Thongpan", "Thongpat", "Thongpol"
]

# Generate random data
data = []

for i in range(num_records):
    # Generate random date within range
    random_days = np.random.randint(0, date_range)
    order_date = start_date + timedelta(days=random_days)
    order_date_str = order_date.strftime('%d/%m/%Y')
    
    # Select random product
    product = np.random.choice(products)
    
    # Generate random quantity
    quantity = np.random.randint(1, 6)
    
    # Calculate price and discount
    unit_price = product["price"]
    discount_pct = np.random.choice([0, 0, 0, 5, 10, 15, 20], p=[0.6, 0.1, 0.1, 0.08, 0.06, 0.04, 0.02])
    discount_amount = (unit_price * discount_pct / 100)
    discounted_price = unit_price - discount_amount
    total_price = discounted_price * quantity
    
    # Generate customer info
    customer_first_name = np.random.choice(first_names)
    customer_last_name = np.random.choice(last_names)
    customer_name = f"{customer_first_name} {customer_last_name}"
    customer_email = f"{customer_first_name.lower()}.{customer_last_name.lower()}@example.com"
    customer_phone = f"0{np.random.randint(6, 10)}{np.random.randint(1000000, 9999999)}"
    
    # Generate location info
    province = np.random.choice(provinces, p=province_weights)
    postal_code = f"{np.random.randint(10000, 99999)}"
    
    # Generate order info
    order_id = f"DD{np.random.randint(100000, 999999)}"
    channel = np.random.choice(channels, p=channel_weights)
    payment_status = np.random.choice(["ชำระครบ", "รอชำระ", "ยกเลิก"], p=[0.85, 0.1, 0.05])
    order_status = "สำเร็จ" if payment_status == "ชำระครบ" else ("รอจัดส่ง" if payment_status == "รอชำระ" else "ยกเลิก")
    
    # Generate shipping info
    tracking_no = f"TH{np.random.randint(10000000, 99999999)}" if order_status != "ยกเลิก" else None
    shipping_method = np.random.choice(["Flash Express", "Kerry Express", "Thailand Post", "J&T Express"])
    shipping_cost = np.random.choice([50, 60, 70, 80, 100])
    
    # Generate payment info
    payment_method = np.random.choice(["Credit Card", "Bank Transfer", "COD", "Prompt Pay", "TrueMoney Wallet"])
    payment_date = order_date + timedelta(days=np.random.randint(0, 3)) if payment_status == "ชำระครบ" else None
    payment_date_str = payment_date.strftime('%d/%m/%Y') if payment_date else None
    
    # Create record
    record = {
        "Unnamed: 0": channel,
        "#": i + 1,
        "ประเภท": "ขายออก",
        "รายการ": order_id,
        "สร้างโดย": "Admin",
        "ชื่อลูกค้า": customer_name,
        "รหัสลูกค้า": np.random.randint(1000, 9999),
        "อีเมลลูกค้า": customer_email,
        "เบอร์โทรศัพท์ลูกค้า": customer_phone,
        "ที่อยู่ลูกค้า": f"{np.random.randint(1, 999)} หมู่ {np.random.randint(1, 20)}, {province}",
        "เลขผู้เสียภาษี": None,
        "อ้างอิง": None,
        "ช่องทางการขาย": channel,
        "วันที่ทำรายการ": order_date_str,
        "ส่วนลด": discount_pct if discount_pct > 0 else None,
        "รายได้จาก Platform": -shipping_cost if channel in ["Lazada", "Shopee"] else None,
        "ค่าส่ง (ที่เรียกเก็บจากลูกค้า)": shipping_cost,
        "มูลค่ารวมก่อนภาษี": total_price,
        "ภาษีมูลค่าเพิ่ม": 0.0,
        "วันส่งสินค้า": None,
        "Tracking No": tracking_no,
        "ช่องทางจัดส่ง": shipping_method,
        "ชื่อผู้รับ": customer_name,
        "เบอร์โทรศัพท์ผู้รับ": customer_phone,
        "อีเมลผู้รับ": None,
        "ที่อยู่/จัดส่ง": f"{np.random.randint(1, 999)} หมู่ {np.random.randint(1, 20)}, {province}",
        "รหัสไปรษณีย์": postal_code,
        "จังหวัด": province,
        "อำเภอ/เขต": None,
        "ตำบล/แขวง": None,
        "มูลค่า": total_price,
        "หมายเหตุ": None,
        "Tag": None,
        "สถานะรายการ": order_status,
        "คลัง/สาขา": "สต๊อกกลาง",
        "สถานะการชำระเงิน": payment_status,
        "ใบกำกับภาษี": None,
        "ช่องทางการชำระเงิน": payment_method,
        "จำนวนเงินที่ชำระ": total_price + shipping_cost if payment_status == "ชำระครบ" else None,
        "วันที่ชำระเงิน": payment_date_str,
        "Payment ID": None,
        "รหัสสินค้า": product["code"],
        "ชื่อสินค้า": product["name"],
        "จำนวน": quantity,
        "ราคาต่อหน่วย": unit_price,
        "ส่วนลดต่อหน่วย": discount_amount,
        "ราคารวม": total_price,
        "ล็อต": None,
        "หมวดหมู่": product["category"]
    }
    
    data.append(record)

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel file
output_file = os.path.join('data', 'dog_days_sales_data.xlsx')
df.to_excel(output_file, index=False)

print(f"Mock data generated and saved to {output_file}")
print(f"Generated {num_records} sales records")
