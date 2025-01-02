import uvicorn
from fastapi import FastAPI
import gradio as gr

fastapi_app = FastAPI()


@fastapi_app.get("/chat")
def read_main():
    return {"message": "This is your main app"}


def greet(name):
    return "Hello " + name + "!"


with gr.Blocks() as demo:
    # 设置输入组件
    name = gr.Textbox(label="Name")
    # 设置输出组件
    output = gr.Textbox(label="Output Box")
    # 设置按钮
    greet_btn = gr.Button("Greet")
    # 设置按钮点击事件
    greet_btn.click(fn=greet, inputs=name, outputs=output)

if __name__ == '__main__':
    app = gr.mount_gradio_app(fastapi_app, demo, path="/gr")
    uvicorn.run(fastapi_app, host='127.0.0.1', port=8000)
