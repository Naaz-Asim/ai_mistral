# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# import openai
# load_dotenv()
#
# if __name__ == "__main__":
#     api_key=os.getenv("OPENAI_API_KEY")
#     openai.base_url = os.getenv("OPENAI_BASE_URL")
#
#     if api_key is None:
#         print('You need to set your MISTRAL_API_KEY environment variable')
#         exit(1)
#
#     model="meta-llama/llama-4-maverick:free"
#
#     client = OpenAI(api_key=api_key)
#
#     response =client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
#             {"role": "user", "content": "Who were the founders of Microsoft?"}
#         ]
#     )
#
#     print(response.model_dump_json(indent=2))
#     print("\nAnswer:", response.choices[0].message.content)
