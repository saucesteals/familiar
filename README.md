# **Familiar**
*Talk to GPT-3 directly in Discord!*

### **Installation**

1. Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Create a bot at [https://discord.com/developers/applications/](https://discord.com/developers/applications/) (Make sure you enable all intents)
3. Clone the repo
   ```sh
   git clone https://github.com/saucesteals/familiar.git
   ```
4. Install requirements
   ```sh
   pip/pip3 install -r requirements.txt
   ```
5. Fill in the template in `env.example`
6. Rename `env.example` to `.env`
7. Start it!
   ```sh
   python/python3 main.py
   ```

### **Usage**

- `!reply [reply]` / `!f [reply]` - send and get a reply from familiar
- `!reset` / `!r` - reset your cached conversation history 
- `!create` / `!c` - allows you to create a customized personality for familiar
- `!export` - export your current conversation
- `!transfer` - transfer someone else's current conversation into yours
- `!ping` - gets familiar's ping to discord

*Note that the `!` prefix will not work if you've specified a custom one in the `.env` file*


## **Contributing**

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## **Honorable Mentions**

   - Huge thanks to the [GPT3-Sandbox](https://github.com/shreyashankar/gpt3-sandbox) team for [this](https://github.com/saucesteals/familiar/blob/main/src/familiarOpenAI/gpt.py)

## **License**

Distributed under the GNU GENERAL PUBLIC License. See `LICENSE` for more information.
