import os
import google.generativeai as genai
import json

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
    upload_to_gemini("./assets/ig/拉麵_1.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/拉麵_2.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/拉麵_3.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/火鍋_1.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/火鍋_2.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/火鍋_3.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/燒肉_1.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/燒肉_2.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/燒肉_3.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/甜點_1.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/甜點_2.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/甜點_3.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/甜點_4.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/甜點_5.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/甜點_6.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/甜點_7.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/甜點_8.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/甜點_9.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/西餐_1.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/西餐_2.jpg", mime_type="image/jpeg"),
    upload_to_gemini("./assets/ig/西餐_3.jpg", mime_type="image/jpeg"),
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

def ai_pick_overlay_image(current_photo_path, category=""):
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
          files[7],
          files[8],
          files[9],
          files[10],
          files[11],
          files[12],
          files[13],
          files[14],
          files[15],
          files[16],
          files[17],
          files[18],
          files[19],
          files[20],
          "\nYou are a professional Instagram foodgram post photographer. Your task is to recommend example food photos according to the user's current food photo and simple description.\n\nI have uploaded 21 example food photos with the following categories: 火鍋, 西餐, 拉麵, 甜點, 燒肉. Each photo is named accordingly, such as 火鍋_1.jpg, 西餐_2.jpg, and so on. Please remember these categories and photo names.\n\nFirst of all, please describe each image in the following format: {photo name}: {description}. Then, when a user uploads a current food photo with a simple description like \"我吃的是 甜點,\" recommend the three most relevant example food photos from the uploaded ones based on the presentation style and the description. **Do not explain anything. Only return the filenames of the three recommended example food photos, separated by commas without spaces, under all circumstances. If there are no matching food photos, still return any three filenames from the uploaded examples.**\n\n**Example output:** 甜點_1.jpg,甜點_3.jpg,甜點_6.jpg",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Here is the description for each image:\n\n火鍋_1.jpg: A hot pot with two different broths, one spicy and one clear, with various meats, vegetables, and noodles around it.\n火鍋_2.jpg: A hot pot with two different broths, one clear and one spicy, with various meats and vegetables around it.\n火鍋_3.jpg: A hot pot with two different broths, one clear and one spicy, with various meats and vegetables around it.\n西餐_1.jpg: A bowl of creamy pasta with a poached egg on top, served with a side of toasted bread and a cup of coffee.\n西餐_2.jpg: A plate of fried chicken, yellow rice, and French fries, served with a side of soup and a glass of milk tea.\n西餐_3.jpg: A plate of poached eggs with a creamy sauce, served on a bed of greens and toasted bread, with a cup of coffee on the side.\n拉麵_1.jpg: A bowl of spicy ramen with pork slices, green onions, and red pepper flakes.\n拉麵_2.jpg: A bowl of ramen with pork slices, green onions, bamboo shoots, and a piece of seaweed.\n拉麵_3.jpg: A bowl of ramen with pork slices, green onions, bamboo shoots, and a soft-boiled egg.\n甜點_1.jpg: A slice of tiramisu topped with chocolate shavings.\n甜點_2.jpg: A plate of crème brûlée with a caramelized sugar crust.\n甜點_3.jpg: A plate of assorted cheesecakes, with a green tea roll in the background.\n甜點_4.jpg: A plate of crème brûlée with a caramelized sugar crust.\n甜點_5.jpg: A box of assorted tarts, including blueberry, spinach, matcha, and strawberry.\n甜點_6.jpg: A slice of cake topped with a fig slice.\n甜點_7.jpg: A slice of cheesecake with a cup of black coffee.\n甜點_8.jpg: Two slices of French toast topped with powdered sugar and a sprig of rosemary.\n甜點_9.jpg: A vegetarian sandwich served with a cup of latte.\n燒肉_1.jpg: A plate of raw beef and pork slices, ready to be grilled on a hotplate.\n燒肉_2.jpg: A plate of raw beef and pork slices, ready to be grilled on a hotplate.\n燒肉_3.jpg: A plate of raw beef and tongue slices, ready to be grilled, served with rice, salad, and soup.\n",
        ],
      },
    ]
  )

  gemini_file = upload_to_gemini(current_photo_path, mime_type="image/jpeg")

  if category != "":
    message_parts = [
      gemini_file,
      f"我吃的是 {category}",
      "**Do not explain anything. Only return the filenames of the three recommended example food photos, separated by commas without spaces, under all circumstances. If there are no matching food photos, still return any three filenames from the uploaded examples.**\n**Example output:** 甜點_1.jpg,甜點_3.jpg,甜點_6.jpg"
    ]
  else:
    message_parts = [
      gemini_file,
      "**Do not explain anything. Only return the filenames of the three recommended example food photos, separated by commas without spaces, under all circumstances. If there are no matching food photos, still return any three filenames from the uploaded examples.**\n**Example output:** 甜點_1.jpg,甜點_3.jpg,甜點_6.jpg"
    ]

  response = chat_session.send_message(message_parts)
  overlay_image_paths = response.text.split(",")
  overlay_image_paths = [f"./assets/ig/{path.strip()}" for path in overlay_image_paths]

  return overlay_image_paths

def ai_choose_warm_tone_parameter(file_path):
  gemini_file = upload_to_gemini(file_path, mime_type="image/jpeg")

  message_parts = [
    gemini_file,
    "User has uploaded a food image and needs to enhance its warm tone. Provide the appropriate image enhancement parameters as a JSON dictionary, focusing on `brightness` and `contrast` values. Ensure that `brightness` is between 1.0 and 1.05, and `contrast` is between 1.15 and 1.25. Return only the JSON object without any explanation or code formatting.",
    "Example output:\n{\"brightness\": 1.03, \"contrast\": 1.2}"
  ]

  response = model.generate_content(message_parts)

  # 使用 json.loads() 安全解析 JSON 字符串
  enhancement_params = json.loads(response.text)

  return enhancement_params

def ai_generate_caption(store_name, items, review):
  response = model.generate_content([
    "你是一位專業的Instagram美食文案撰寫者。你的任務是根據用戶提供的店名、品項和心得，生成一篇適合在Instagram上發布的美食貼文文案。\n要求：\n1. 文案需包含餐廳名稱、品項(每個品項獨立成行，通常以逗點或頓點區分)以及簡短的心得，語氣輕鬆且富有熱情。\n2. 請參考範例風格，但避免直接模仿範例中的句式結構，鼓勵文案中使用多樣化的表達方式與詞彙，讓每一篇文案都有其獨特性和創意。\n3. 適當插入表情符號（emoji），數量適中，與文案內容匹配，但表情符號的選擇和位置可以隨情境自由變化。\n4. 文案末尾需加上相關的標籤（hashtags），格式與範例相似，但可以自由選擇不同的標籤來保持變化性。\n特別提醒：你可以使用不同的語氣、句型結構和描述方式來呈現同一主題，讓每篇文案看起來都新穎獨特。可以以心得來豐富文案，但保持內容簡潔不冗長。",
    "店名: 幻猻家珈琲 Pallas Cafe",
    "品項: 小花奇諾、焦糖布丁",
    "心得: 特調咖啡香甜可口，但對我而言稍微太甜了一點。",
    "output: 📍 幻猻家珈琲 Pallas Cafe\n-\n✨小花奇諾\n✨焦糖布丁\n-\n久違的跑咖 看到週年限定的特調咖啡就忍不住點了 洋甘菊+蜂蜜+伯爵茶+濃縮 聞起來是清新的香甜 但喝起來覺得太甜了一點 可能真的長了年紀不再適合小時候會愛的甜咖啡\n布丁好大一份啊 甜度偏低（還是先喝了咖啡的關係？）不是綿綿入口即化布丁 是我偏愛的有點滑有點口感的那種\n下次想試試手沖還有鹹食\n-\n\n#taiwanfood#美食#幻猻家珈琲",
    "店名: Coffeeloft-咖啡工寓",
    "品項: 拿鐵",
    "心得: 環境舒適，適合放鬆。",
    "output: 📍 Coffeeloft-咖啡工寓\n-\n✨拿鐵\n-\n台東市區咖啡店兼民宿\n環境好舒適\n-\n\n#taiwanfood#foodie#cafe#美食#Coffeeloft咖啡公寓",
    "店名: 點二咖啡",
    "品項: 法式吐司、黑糖拿鐵",
    "心得: 法式吐司趁熱吃口感絕佳，黑糖拿鐵甜度適中，值得一試。",
    "output: 📍點二咖啡\n-\n✨法式吐司\n✨黑糖拿鐵\n-\n隱藏在二樓還是很多人耶，老闆有些小規矩去之前記得先看看\n🍴法式吐司看起來不起眼，但趁熱吃很厲害欸，濕度與口感控制的剛好，一點濕口感偏綿密但也有嚼勁，配糖漿也不會太甜，蠻喜歡的😍雖然冷掉之後不好吃😂\n🍴黑糖拿鐵好喝，黑糖在上層撲滿，配上拿鐵不會過甜，黑糖香氣也足夠\n-\n\n#taiwanfood#igfood#popyummy#foodie#coffee#cafe#afternoontea#latte#美食#咖啡#甜點#法式吐司#點二咖啡",
    f"店名: {store_name}",
    f"品項: {items}",
    f"心得: {review}",
    "output: ",
  ])

  caption = response.text
  
  return caption

def ai_generate_caption_with_audio(audio_file_path):
  gemini_file = upload_to_gemini(audio_file_path, mime_type="audio/aac")

  message_parts = [
    gemini_file,
    "你是一位專業的Instagram美食文案撰寫者。你的任務是根據用戶提供音檔中的店名、品項和心得，生成一篇適合在Instagram上發布的美食貼文文案。\n要求：\n1. 文案需包含餐廳名稱、品項(每個品項獨立成行，通常以逗點或頓點區分)以及簡短的心得，語氣輕鬆且富有熱情。\n2. 請參考範例風格，但避免直接模仿範例中的句式結構，鼓勵文案中使用多樣化的表達方式與詞彙，讓每一篇文案都有其獨特性和創意。\n3. 適當插入表情符號（emoji），數量適中，與文案內容匹配，但表情符號的選擇和位置可以隨情境自由變化。\n4. 文案末尾需加上相關的標籤（hashtags），格式與範例相似，但可以自由選擇不同的標籤來保持變化性。\n特別提醒：你可以使用不同的語氣、句型結構和描述方式來呈現同一主題，讓每篇文案看起來都新穎獨特。可以以心得來豐富文案，但保持內容簡潔不冗長。",
    "**因為是音檔，所以你需要先分析音檔中的店名、品項和心得，然後生成一篇適合的文案。**"
    "店名: 幻猻家珈琲 Pallas Cafe",
    "品項: 小花奇諾、焦糖布丁",
    "心得: 特調咖啡香甜可口，但對我而言稍微太甜了一點。",
    "output: 📍 幻猻家珈琲 Pallas Cafe\n-\n✨小花奇諾\n✨焦糖布丁\n-\n久違的跑咖 看到週年限定的特調咖啡就忍不住點了 洋甘菊+蜂蜜+伯爵茶+濃縮 聞起來是清新的香甜 但喝起來覺得太甜了一點 可能真的長了年紀不再適合小時候會愛的甜咖啡\n布丁好大一份啊 甜度偏低（還是先喝了咖啡的關係？）不是綿綿入口即化布丁 是我偏愛的有點滑有點口感的那種\n下次想試試手沖還有鹹食\n-\n\n#taiwanfood#美食#幻猻家珈琲",
    "店名: Coffeeloft-咖啡工寓",
    "品項: 拿鐵",
    "心得: 環境舒適，適合放鬆。",
    "output: 📍 Coffeeloft-咖啡工寓\n-\n✨拿鐵\n-\n台東市區咖啡店兼民宿\n環境好舒適\n-\n\n#taiwanfood#foodie#cafe#美食#Coffeeloft咖啡公寓",
    "店名: 點二咖啡",
    "品項: 法式吐司、黑糖拿鐵",
    "心得: 法式吐司趁熱吃口感絕佳，黑糖拿鐵甜度適中，值得一試。",
    "output: 📍點二咖啡\n-\n✨法式吐司\n✨黑糖拿鐵\n-\n隱藏在二樓還是很多人耶，老闆有些小規矩去之前記得先看看\n🍴法式吐司看起來不起眼，但趁熱吃很厲害欸，濕度與口感控制的剛好，一點濕口感偏綿密但也有嚼勁，配糖漿也不會太甜，蠻喜歡的😍雖然冷掉之後不好吃😂\n🍴黑糖拿鐵好喝，黑糖在上層撲滿，配上拿鐵不會過甜，黑糖香氣也足夠\n-\n\n#taiwanfood#igfood#popyummy#foodie#coffee#cafe#afternoontea#latte#美食#咖啡#甜點#法式吐司#點二咖啡",
    "output: ",
  ]

  response = model.generate_content(message_parts)

  caption = response.text

  return caption