```
response = model.generate_content(["Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.", img], stream=True)
response.resolve()
```

[text](https://github.com/google-gemini/cookbook/blob/main/quickstarts/File_API.ipynb)

[text](https://ai.google.dev/gemini-api/docs/document-processing?hl=zh-tw&lang=python)


驗證 PDF 檔案上傳及取得中繼資料
您可以驗證 API 是否已成功儲存上傳的檔案，並取得其 透過 SDK 呼叫 files.get 來更新中繼資料僅限 name (及 副檔名為 uri) 重複。只有在符合以下條件時，才使用「display_name」來識別檔案 以及自己的特色

file = genai.get_file(name=sample_file.name)
print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

根據您的用途，您可以將 URI 儲存在結構中，例如 dict 或資料庫。

可列出檔案
您可以使用 File API 列出透過 File API 上傳的所有檔案及其 URI files.list_files():

```
# List all files
for file in genai.list_files():
    print(f"{file.display_name}, URI: {file.uri}")
```