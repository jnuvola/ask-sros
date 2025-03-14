from flask import Flask, render_template, request, jsonify
import paramiko
import os
import re
import json
import datetime
import time
from openai import OpenAI

app = Flask(__name__)


def load_prompt(filename):
    try:
        with open(os.path.join("prompts", filename), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Prompt file {filename} not found in the prompts directory"
        )
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {filename}")


def get_cli_command(natural_language_question: str) -> str:
    client = OpenAI()

    nokia_prompt = load_prompt("router_input.json")

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": nokia_prompt["system_content"],
            },
            {
                "role": "user",
                "content": f"{natural_language_question} (UTC timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()})",
            },
        ],
        temperature=0.1,
        top_p=0.1,
        max_tokens=500,
        model=os.environ.get("OPENAI_MODEL_NAME"),
    )
    command_markdown = response.choices[0].message.content.strip()
    match = re.search(r"```sql\s*(.*?)\s*```", command_markdown, re.DOTALL)
    command = match.group(1) if match else command_markdown
    return command


def parse_cli_output(device_output: str, natural_language_question: str) -> str:
    client = OpenAI()

    router_prompt = load_prompt("router_output.json")

    system_content = router_prompt["system_content"].format(
        user_question=natural_language_question
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": device_output,
            },
        ],
        temperature=0.2,
        top_p=0.2,
        max_tokens=500,
        model=os.environ.get("OPENAI_MODEL_NAME"),
    )
    human_readable = response.choices[0].message.content.strip()
    return human_readable


def execute_cli_command(command: str) -> str:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            os.environ.get("ASKSROS_ROUTER_ADDRESS"),
            port=os.environ.get("ASKSROS_ROUTER_PORT"),
            username=os.environ.get("ASKSROS_ROUTER_USERNAME"),
            password=os.environ.get("ASKSROS_ROUTER_PASSWORD"),
        )
        channel = client.invoke_shell()
        time.sleep(1)

        if channel.recv_ready():
            channel.recv(1024)

        if "|" not in command:
            channel.send(command + " | no-more\n")
        else:
            channel.send(command + "\n")
        time.sleep(2)

        output = ""
        while channel.recv_ready():
            output += channel.recv(1024).decode("utf-8")
        return output
    except Exception as e:
        return f"Error executing command: {e}"
    finally:
        client.close()


def query_router(question: str) -> dict:
    command = get_cli_command(question)
    raw_output = execute_cli_command(command)
    explanation = parse_cli_output(raw_output, question)
    return {"command": command, "raw_output": raw_output, "explanation": explanation}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided."}), 400
    try:
        result = query_router(question)
        return jsonify(result)
    except Exception as e:
        error_msg = str(e)
        return jsonify({"error": error_msg}), 500


if __name__ == "__main__":
    app.run(debug=True)
