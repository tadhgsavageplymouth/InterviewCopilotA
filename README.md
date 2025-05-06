# InterviewCopilotA

> **Humanoid robot–powered mock interviews with real-time emotional insight**

## Features
- **Domain-aware questioning** – Uses OpenAI GPT-4 to generate tailored interview questions for roles such as *Software Engineer* or *Doctor*.
- **Real-time affect sensing** – External webcam + LibreFace/DeepFace classify Ekman emotions to gauge stress and engagement.
- **Speech & gestures** – NAO delivers questions via TTS while maintaining eye contact and subtle idle motions for social presence.
- **Session logging** – Stores all dialogue turns, emotion timelines and robot actions for later analysis.

## Quick-start

```bash
# 1. Clone
git clone https://github.com/tadhgsavageplymouth/InterviewCopilotA.git
cd InterviewCopilotA

# 2. Create virtual environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Set environment variables
export OPENAI_API_KEY=YOUR_KEY
export NAO_IP=192.168.1.42  # robot’s IP

# 4. Run server
python server/app.py
```

### Running the NAO client
Upload `robot/nao_client.py` to NAO (or run inside Choregraphe) and execute:

```bash
python nao_client.py --server http://<HOST>:5000
```

## Project status
- Core dialogue loop ✅  
- Emotion recognition prototype ✅  
- Adaptive questioning ⏳ (planned)  
- React dashboard ⏳ (under development)  

## Contributing
Pull requests welcomed! Please open an issue first to discuss major changes.

## Acknowledgements
COMP3018 Human-Robot Interaction module, Plymouth University.  
SoftBank Robotics for NAO hardware.
