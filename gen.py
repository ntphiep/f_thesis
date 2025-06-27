import sys
from google import genai
import time
import asyncio
import functools
import aiofiles
import re
from tenacity import retry, stop_after_attempt, wait_fixed


client = genai.Client(api_key="")
# chat = client.chats.create(model="gemini-2.0-flash")

if len(sys.argv) > 1:
    fnum = sys.argv[1] 
    
def contains_chinese(text: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', text))


async def run_in_threadpool(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, functools.partial(func, *args))


# @retry(stop=stop_after_attempt(4), wait=wait_fixed(10))
def gen(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""
        Bạn hiều thế nào là 'văn phong' chứ? tôi đang làm một mô hình NLP liên quan đến 
        chuyển đổi văn phong, nhờ bạn generate data tiếng Việt giúp tôi nhé, giờ tôi sẽ đưa cho bạn một 
        câu bất kì, bạn hãy tạo cho tôi các câu mới có cùng ý nghĩa nhưng khác văn phong với câu gốc,
        trong đó câu đầu tiên mang văn phong bình dân, xuồng xã, có thân mật, giống như kiểu văn nói, trò chuyện hằng ngày
        câu thứ hai mang văn phong như đang giống như giang hồ, đường phố, xuồng xã, không tỏ ra thân mật, đôi lúc có thể tục tĩu
        câu thứ ba mang văn phong trang trọng, lịch sự, nghiêm túc như kiểu các loại văn bản hành chính hoặc phát biểu tại các sự kiện, hội nghị, hội thảo có tính nghiêm túc, trang trọng;
        câu thứ tư mang văn phong như trong phim kiếm hiệp, cổ trang, đạo lý, tu tiên kiểu như trong phim cổ trang Trung Quốc , sử dụng đan xen các từ Hán Việt (NOTE: từ Hán Việt latin chứ không phải Hán tự, kí tự chữ Trung Quốc nhé. KHÔNG để các kí tự chữ Trung Quốc, Hán tự nhé, để Hán Việt latin thôi, tuyệt đối không được để Hán tự, tiếng Trung nhé trong output nhé).
        Bây giờ tôi sẽ đưa cho bạn một câu, bạn hãy tạo cho tôi một cặp câu như vậy nhé. Nhớ là mấy kí tự đặc biệt không liên quan thì nhớ bỏ đi nhé, chỉ giữ lại phần nội dung text mang ý nghĩa.
        Các từ tiếng nước ngoài thì hãy để nguyên, không cần dịch sang tiếng Việt nhé.
        Câu của tôi là: '{text}'. Hãy đưa ra output của bạn theo định dạng JSON như sau: 
        {{"source": "...", "1": "...", "2": "...", "3": "...", "4": "..."}}, nếu input có nhiều câu thì cứ trả về định dạng như vậy cho từng câu và cách nhau bằng dấu ,
        không cần giải thích hay bất cứ gì thêm nhé, chỉ cần đưa ra đúng y như địng dạng vậy thôi, không cần nói gì khác nhé.
        KHÔNG để các kí tự chữ Trung Quốc, Hán tự nhé, để Hán Việt latin thôi, tuyệt đối không được để Hán tự, tiếng Trung nhé trong output nhé.
        À nhớ đừng cho kí tự gì khác, kể cả [ và ] nhé. Đảm bảo đúng định dạng JSON, không lỗi gì nhé để sau này tôi dễ xử lý.
        Nhớ kỹ là phải đúng định dạng JSON chuẩn đấy, nhớ những lời của tôi, tuyệt đối KHÔNG có bất cứ Hán tự, chữ tiếng Trung nào trong output
        """
    )
    return(response.text)


@retry(wait=wait_fixed(10), stop=stop_after_attempt(5))
async def process_batch(batch):
    gen_data = await run_in_threadpool(gen, batch)
    gen_data =  gen_data.replace('```json', '').replace('```', '').strip()
    return gen_data  if not contains_chinese(gen_data) else await process_batch(batch)

async def main_batch_with_timeout(batch):
    try:
        return await asyncio.wait_for(process_batch(batch), timeout=600)
    except asyncio.TimeoutError:
        print(f"Timeout mẹ mày rồi: batch {batch}")
        return ""



async def main():
    # Read the dataset file
    batch_size = 5
    batches = []
    
    # Đọc file async
    async with aiofiles.open(f'chunks/chunk_{fnum}.txt', 'r', encoding='utf-8') as f:
        batch = []
        async for line in f:
            batch.append(line)
            if len(batch) == batch_size:
                batches.append(batch)
                batch = []
    
    # Process each batch
    async with aiofiles.open(f'chunks_out/chunk_{fnum}.json', 'w', encoding='utf-8') as f_out:
        semaphore = asyncio.Semaphore(500)
        async def process_with_semaphore(batch):
            async with semaphore:
                gen_data = await main_batch_with_timeout(batch)
                print(gen_data)
                await f_out.write(gen_data + ',\n')
                # if not await contains_chinese(gen_data):
                #     await f_out.write(gen_data + ',\n')
                # else:
                #     async with aiofiles.open(f'mismatch/chunk_{fnum}_err.json', 'a', encoding='utf-8') as f_err:
                #         await f_err.write(gen_data + ',\n')

        await asyncio.gather(
            *[process_with_semaphore(batch) for batch in batches]
        )


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    
    chunk_path = f'chunks_out/chunk_{fnum}.json'

    with open(chunk_path, 'r+', encoding='utf-8') as f:
        raw = f.read().strip()
        raw = f"[{raw[:-1]}]"  # xoá kí tự cuối và wrap []
        f.seek(0)
        f.write(raw)

    print(f"✅ Thành công, ghi vào: {chunk_path}")
    print(f"Thời gian thực thi: {end_time - start_time} giây")
