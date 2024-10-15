import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Get a list of uploaded files
uploaded_files = dict()
for file in genai.list_files():
  uploaded_files[file.display_name] = file

# Uploader function
def upload_to_gemini(path, mime_type=None):
  display_name = os.path.basename(path)

  if display_name in uploaded_files:
    print(f"File '{display_name}' already exists in Gemini.")
    return uploaded_files[display_name]
  
  file = genai.upload_file(path, mime_type=mime_type, display_name=display_name)
  print(f"Uploaded file '{file.name}'({file.display_name}) as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # system_instruction=''
)

files = [
  upload_to_gemini("./assets/milk/1.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/2.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/3.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/4.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/5.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/6.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/7.png", mime_type="image/png"),
]

def ai_overlay_number(file_path):
  chat_session = model.start_chat(
    history=[
      {
        "role": "user",
        "parts": [
          files[0],
          files[1],
          files[2],
          files[3],
          files[4],
          files[5],
          files[6],
          "Here's posing 7 images, they are used to be overlapped on an user's camera to help them posing when taking photos. They are indexed with Image 1 to Image 7. In each image, there are white lines that show an example posing, and the rest of the picture are leaved blank/transparent. I want you to remember these 7 posing images, analyze and response me with their posing features (for example, Image 1: two people sitting side by side, drink close to their head).",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Image 1: two people sitting side by side, drink close to their head\nImage 2: one person with one arm raised, holding a drink\nImage 3: one person sitting, holding a drink \nImage 4: one person standing, holding a drink in one hand, the other hand is on their hip\nImage 5: two people sitting side by side, drink close to their head\nImage 6: one person sitting, holding a drink \nImage 7: one person sitting, holding a drink",
        ],
      },
      {
        "role": "user",
        "parts": [
          "Later, on the following prompts, I would give you one current camera view photo on each one prompt. You have to response me with the most suitable posing image number you choose according to the current camera view photo. Your response should contain only one integer to indicate the pose image number (for example, if your answer is Image 1, you would simply response me with 1). You shall not explain the choice for me. If you understand, tell me again what I just mentioned to you.",
        ],
      },
      {
        "role": "model",
        "parts": [
          "You will give me a camera view photo for each prompt, and I will respond with the most suitable posing image number (from 1 to 7) based on the photo. I will not explain my choice. \n",
        ],
      },
    ]
  )

  gemini_file = upload_to_gemini(file_path, mime_type="image/jpeg")
  message_parts = [
    gemini_file,
    "Here is one current camera view photo. Respond me with the most suitable pose image number."
  ]
  response = chat_session.send_message(message_parts)
  return response.text

def ai_pick_overlay_image(file_path):
  # randomly pick one image under /assets/ig/cake_coffee
  import random
  image_files = os.listdir("./assets/ig/cake_coffee")
  image_file = random.choice(image_files)
  image_path = f"./assets/ig/cake_coffee/{image_file}"

  return image_path

def ai_generate_caption(store_name, items, review):
  response = model.generate_content([
    "你是一位專業的Instagram美食文案撰寫者。你的任務是根據用戶提供的店名、品項和心得，生成一篇適合在Instagram上發布的美食貼文文案。\n要求：\n1. 文案需包含餐廳名稱、品項以及簡短的心得，語氣輕鬆且富有熱情。\n2. 請參考範例風格，但避免直接模仿範例中的句式結構，鼓勵文案中使用多樣化的表達方式與詞彙，讓每一篇文案都有其獨特性和創意。\n3. 適當插入表情符號（emoji），數量適中，與文案內容匹配，但表情符號的選擇和位置可以隨情境自由變化。\n4. 文案末尾需加上相關的標籤（hashtags），格式與範例相似，但可以自由選擇不同的標籤來保持變化性。\n特別提醒：你可以使用不同的語氣、句型結構和描述方式來呈現同一主題，讓每篇文案看起來都新穎獨特。可以以心得來豐富文案，但保持內容簡潔不冗長。",
    "店名: 幻猻家珈琲 Pallas Cafe",
    "品項: 小花奇諾、焦糖布丁",
    "心得: 特調咖啡香甜可口，但對我而言稍微太甜了一點。",
    "output: 📍 幻猻家珈琲 Pallas Cafe\n-\n✨小花奇諾\n✨焦糖布丁\n-\n久違的跑咖 看到週年限定的特調咖啡就忍不住點了 洋甘菊+蜂蜜+伯爵茶+濃縮 聞起來是清新的香甜 但喝起來覺得太甜了一點 可能真的長了年紀不再適合小時候會愛的甜咖啡\n布丁好大一份啊 甜度偏低（還是先喝了咖啡的關係？）不是綿綿入口即化布丁 是我偏愛的有點滑有點口感的那種\n下次想試試手沖還有鹹食\n-\n\n#taiwanfood#Taipeifood#台北#台北美食#大稻埕咖啡廳#台北咖啡#幻猻家珈琲",
    "店名: Coffeeloft-咖啡工寓",
    "品項: 拿鐵",
    "心得: 環境舒適，適合放鬆。",
    "output: 📍 Coffeeloft-咖啡工寓\n-\n✨拿鐵\n-\n台東市區咖啡店兼民宿\n環境好舒適\n-\n\n#taiwanfood#Taitungfood#foodie#cafe#台東#台東美食#台東咖啡#Coffeeloft咖啡公寓",
    "店名: 點二咖啡",
    "品項: 法式吐司、黑糖拿鐵",
    "心得: 法式吐司趁熱吃口感絕佳，黑糖拿鐵甜度適中，值得一試。",
    "output: 📍點二咖啡\n-\n✨法式吐司\n✨黑糖拿鐵\n-\n隱藏在二樓還是很多人耶，老闆有些小規矩去之前記得先看看\n🍴法式吐司看起來不起眼，但趁熱吃很厲害欸，濕度與口感控制的剛好，一點濕口感偏綿密但也有嚼勁，配糖漿也不會太甜，蠻喜歡的😍雖然冷掉之後不好吃😂\n🍴黑糖拿鐵好喝，黑糖在上層撲滿，配上拿鐵不會過甜，黑糖香氣也足夠\n-\n\n#taiwanfood#Taipeifood#igfood#popyummy#foodie#coffee#cafe#afternoontea#latte#台北#台北美食#台北咖啡#台北甜點#中山區美食#法式吐司#點二咖啡",
    f"店名: {store_name}",
    f"品項: {items}",
    f"心得: {review}",
    "output: ",
  ])

  caption = response.text
  
  return caption