from turtle import st
from flask import cli
from google import genai
import time
import asyncio
import functools
import concurrent.futures
import aiofiles


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
        câu thứ ba mang văn phong trang trọng, lịch sự, nghiêm túc như kiểu đang phát biểu tại các sự kiện, hội nghị, hội thảo có tính nghiêm túc, trang trọng;
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




async def run_in_threadpool(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, functools.partial(func, *args))



async def process_batch(batch, ):
    gen_data = await run_in_threadpool(gen, batch)
    gen_data = gen_data.replace('```json', '').replace('```', '').replace("'", '"').strip()
    return gen_data



async def main():
    # Read the dataset file
    batch_size = 4
    batches = []

    
    # Đọc file async
    async with aiofiles.open('hic.txt', 'r', encoding='utf-8') as f:
        batch = []
        async for line in f:
            batch.append(line)
            if len(batch) == batch_size:
                batches.append(batch)
                batch = []
            
    
    # Process each batch
    async with aiofiles.open('clm.json', 'w', encoding='utf-8') as f_out:
        semaphore = asyncio.Semaphore(300)
        async def process_with_semaphore(batch):
            async with semaphore:
                gen_data = await process_batch(batch)
                print(gen_data)
                await f_out.write(gen_data + ',\n')
    

        await asyncio.gather(
            *[process_with_semaphore(batch) for batch in batches]
        )


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Thời gian thực thi: {end_time - start_time} giây")