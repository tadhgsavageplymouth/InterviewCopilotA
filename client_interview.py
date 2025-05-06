#!/usr/bin/env python3
"""
Interview-copilot client: sends ChatGPT’s questions to NAO and
passes your spoken answers back to ChatGPT for the next follow-up.
"""

import os
import socket
import time
from pathlib import Path

import openai
from dotenv import load_dotenv

SERVER_IP   = "169.254.242.81"       
SERVER_PORT = 10000
MODEL       = "gpt-4o-mini"          
BUFF_SIZE   = 4096

load_dotenv()  
openai.api_key = os.getenv("OPENAI_API_KEY")  

SYSTEM_PROMPT = (
    "You are an interview copilot speaking through a humanoid robot. "
    "Your job is to ask concise follow-up questions that keep digging deeper. "
    "NEVER answer on the interviewee’s behalf; only ask the next question. "
    "Keep each question well under 100 characters so the robot can say it clearly."
)

def ask_openai(messages):
    """Send the conversation to ChatGPT and return the next question (string)."""
    resp = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=60,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

def speak_via_nao(sock, text):
    """Send text to NAO and wait for its ACK."""
    sock.sendall(text.encode("utf-8"))
    _ = sock.recv(BUFF_SIZE)  

def main():
    if openai.api_key is None:
        raise SystemExit("⛔  OPENAI_API_KEY not set — create .env or export the variable.")

    convo = [{"role": "system", "content": SYSTEM_PROMPT}]

    with socket.create_connection((SERVER_IP, SERVER_PORT)) as sock:
        print(f"✅  Connected to NAO at {SERVER_IP}:{SERVER_PORT}")


        first_q = ask_openai(convo + [{"role": "assistant", "content": ""}])
        print("NAO asks:", first_q)
        speak_via_nao(sock, first_q)
        convo.append({"role": "assistant", "content": first_q})

        while True:
            user_answer = input("\n👤 Your answer (or 'exit'): ").strip()
            if user_answer.lower() == "exit":
                print("👋  Ending session.")
                break

            convo.append({"role": "user", "content": user_answer})
            follow_up = ask_openai(convo)
            convo.append({"role": "assistant", "content": follow_up})

            print("NAO asks:", follow_up)
            speak_via_nao(sock, follow_up)

            time.sleep(0.5)

if __name__ == "__main__":
    main()
