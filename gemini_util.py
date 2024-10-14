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

def ai_generate_caption(text):
  chat_session = model.start_chat(
    history=[
      {
        "role": "user",
        "parts": [
          "你是一個替麥香奶茶寫文案的人，請給我你50個形容奶茶好喝的形容詞。",
        ],
      },
      {
        "role": "model",
        "parts": [
          "## 50個形容麥香奶茶好喝的形容詞：\n\n**香氣：**\n\n1. 茶香濃郁\n2. 麥香醇厚\n3. 香氣撲鼻\n4. 芬芳迷人\n5. 淡淡清香\n6. 溫潤香甜\n7. 香氣四溢\n8. 茶味鮮明\n9. 麥香誘人\n10. 香氣迷醉\n\n**口感：**\n\n11. 滑順綿密\n12. 濃郁香醇\n13. 口感豐富\n14. 柔順香甜\n15. 茶味甘醇\n16. 濃郁香滑\n17. 醇厚香濃\n18. 口感細膩\n19. 柔滑順口\n20. 茶香滿溢\n\n**甜蜜度：**\n\n21. 微甜可口\n22. 甜度適中\n23. 清甜爽口\n24. 恰到好處\n25. 甜而不膩\n26. 微微香甜\n27. 溫柔甜蜜\n28. 甜味濃郁\n29. 沁人心脾\n30. 甜蜜幸福\n\n**感受：**\n\n31. 令人滿足\n32. 回味無窮\n33. 溫暖人心\n34. 舒緩身心\n35. 幸福感滿滿\n36. 令人愉悅\n37. 充滿活力\n38. 精神抖擻\n39. 讓人放鬆\n40. 充滿能量\n\n**其他：**\n\n41. 古典風味\n42. 懷舊經典\n43. 傳統美味\n44. 獨特風味\n45. 無可取代\n46. 令人上癮\n47. 欲罷不能\n48. 完美搭配\n49. 值得回味\n50. 百喝不厭\n\n**額外提示：**\n\n* 可以根據不同的麥香奶茶產品，加入更具體的形容詞，例如：\n    * 麥香奶茶-經典風味：經典、懷舊、傳統、純粹\n    * 麥香奶茶-減糖：清爽、健康、低卡、清爽\n    * 麥香奶茶-新口味：創新、獨特、驚喜、令人驚豔\n\n希望這些形容詞能幫助你寫出更吸引人的麥香奶茶文案！",
        ],
      },
      {
        "role": "user",
        "parts": [
          "在接下來的對話中，我會給你一個替麥香奶茶照片所想的簡短文案。請回復我你根據這個簡短文案，參考上述所提到的麥香奶茶的形容詞，所完成的完整的麥香奶茶照片文案。字數介於150字上下，請加入少許的emoji，以及在文案最後加上hashtags。請切記，無須回復完整文案以外的文字，只需要直接給出完整完案即可。如果你懂了，請回復我剛剛告訴你的需求。",
        ],
      },
      {
        "role": "model",
        "parts": [
          "懂了。請您提供簡短文案，我會幫您完成完整文案。 \n",
        ],
      },
    ]
  )

  message_parts = [
    text,
    "根據上述所提到的麥香奶茶的形容詞，所完成的完整的麥香奶茶照片文案。字數介於150字上下，請加入少許的emoji，以及在文案最後加上hashtags。"
  ]
  response = chat_session.send_message(message_parts)
  return response.text