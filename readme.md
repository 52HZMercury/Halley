---

# README.md

# ☄️ Halley - The Economist Auto-Deliver

**Halley** is an automated Python pipeline designed to foster long-term English language growth by ensuring a steady, weekly supply of *The Economist* magazine directly to your inbox.

## 🌌 Why "Halley"?

The project is named after **Halley's Comet**. Just as the comet is famous for its predictable, periodic return to Earth, this project operates on a precise weekly cycle. It serves as a symbolic reminder that language mastery is not a sprint, but a result of **periodic, consistent habits**.

## 🎓 Core Mission: English Proficiency

The primary goal of Halley is **English language enhancement**. *The Economist* is renowned for its sophisticated vocabulary, complex sentence structures, and global perspective. By automating the fetching and delivery process, Halley removes the "friction" of manual searching, allowing you to dedicate 100% of your effort to reading and learning.

## 🛠️ Key Features

* **Periodic Automation**: The system autonomously triggers every Saturday at 20:00, synchronized with the magazine's release cycle.
* **Smart Retrieval**: Automatically calculates the date of the latest issue and downloads the high-quality `.epub` version.
* **Seamless Delivery**: Uses SMTP to send the magazine as an attachment to your designated email addresses (perfect for Kindle or tablet reading).
* **Reliable Infrastructure**: Includes built-in proxy support for stable downloads and error-handling to ensure the workflow only proceeds if the file is successfully fetched.

## 🏗️ Project Structure

The project is composed of three specialized modules:

1. **`auto_runner.py` (The Heart)**: A long-running background scheduler that coordinates the entire workflow.
2. **`download_economist.py` (The Gatherer)**: Handles URL construction, directory management, and the actual file download from curated repositories.
3. **`send_email.py` (The Messenger)**: A secure SMTP client that delivers the latest file to your mailing list.

## 🚀 Quick Start

### 1. Prerequisites

* Python 3.x
* Required libraries: `pip install requests schedule`

### 2. Configuration

* **Download**: Set your proxy settings in `download_economist.py` if necessary.
* **Email**: Update `SENDER_EMAIL`, `SENDER_PASSWORD`, and `RECEIVER_EMAILS` in `send_email.py`.

### 3. Running the Bot

Simply start the orchestrator:

```bash
python auto_runner.py

```

The "Halley" cycle will begin, and you can expect your first issue this coming Saturday.

---

## 📝 License

This project is for personal educational and language learning purposes. Please respect the copyright of the content providers.