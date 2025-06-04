from flask import cli
from google import genai
import time


client = genai.Client(api_key="AIzaSyBeq62Pg1yKQ6CFXMDR8g1WCMxpm4m5yY8")
# chat = client.chats.create(model="gemini-2.0-flash")

def gen(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""
        Bạn hiều thế nào là 'văn phong' chứ? tôi đang làm một mô hình NLP liên quan đến 
        chuyển đổi văn phong, nhờ bạn generate data tiếng Việt giúp tôi nhé, giờ tôi sẽ đưa cho bạn một 
        câu bất kì, bạn hãy tạo cho tôi các câu mới có cùng ý nghĩa nhưng khác văn phong với câu gốc,
        trong đó câu đầu tiên mang văn phong bình dân, xuồng xã, có thân mật, giống như kiểu văn nói, trò chuyện hằng ngày
        câu thứ hai mang văn phong như đang giống như giang hồ, đường phố, xuồng xã, không tỏ ra thân mật, đôi lúc có thể tục tĩu
        câu thứ ba mang văn phong trang trọng, lịch sự, nghiêm túc như kiểu văn bản tại các sự kiện, hội nghị, hội thảo có tính nghiêm túc, trang trọng;
        câu thứ năm mang văn phong như trong phim kiếm hiệp, cổ trang, đạo lý, tu tiên kiểu như trong phim cổ trang Trung Quốc , sử dụng đan xen các từ Hán Việt.
        Bây giờ tôi sẽ đưa cho bạn một câu, bạn hãy tạo cho tôi một cặp câu như vậy nhé. Nhớ là mấy kí tự đặc biệt không liên quan thì nhớ bỏ đi nhé, chỉ giữ lại phần nội dung text mang ý nghĩa.
        Các từ tiếng nước ngoài thì hãy để nguyên, không cần dịch sang tiếng Việt nhé.
        Câu của tôi là: '{text}'. Hãy đưa ra output của bạn theo định dạng JSON như sau: 
        {{'source': '...', '1': '...', '2': '...', '3': '...', '4': '...'}}, nếu input có nhiều câu thì cứ trả về định dạng như vậy cho từng câu và cách nhau bằng dấu ,
        không cần giải thích hay bất cứ gì thêm nhé, chỉ cần đưa ra đúng y như địng dạng vậy thôi, không cần nói gì khác nhé.
        Cảm ơn bạn nhé, bạn thực sự là một model thông minh và hữu ích!
        """
    )

    return(response.text)




def process_batch(batch, i=0):
    gen_data = gen(batch)
    gen_data = gen_data.replace('```json', '').replace('```', '').replace("'", '"').strip()
    with open(f'pro.json', 'a', encoding='utf-8') as f:
        f.write(gen_data + ',\n')
    # print(gen_data)


def main():
    # Read the dataset file
    
    with open('s.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    
    batch_size = 4
    for i in range(0, len(lines), batch_size):
        batch = lines[i:i + batch_size]
        print(batch)
        
        try:
            process_batch(batch, i)
            print("\n" + "="*50 + "\n")  # Separatoif __name__ == "__main__":
            
            time.sleep(1)  # Sleep for 1 second between batches
        
        
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(20)
            
    
        


if __name__ == "__main__":
    main()
