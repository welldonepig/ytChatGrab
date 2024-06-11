# YouTube Live Chat Fetcher

This project is a Python application that fetches live chat messages from a YouTube live stream and saves them to a text file. It features a graphical user interface (GUI) built with `tkinter` for easy input of API Key and YouTube video URL, as well as options to start and stop fetching chat messages, and set the save file location.

## Features

- Fetches live chat messages from a YouTube live stream.
- GUI for inputting YouTube API Key and video URL.
- Start and stop fetching chat messages.
- Set and display the location of the save file.
- Error handling and informative messages.

## Requirements

- Python 3.6 or later
- `google-api-python-client` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. Install the required Python libraries:

    ```bash
    pip install google-api-python-client
    ```

## Usage

1. Run the application:

    ```bash
    python youtube-live-chat-gui.py
    ```

2. Enter your YouTube API Key and the URL of the YouTube video you want to fetch chat messages from.

3. Click "開始" to start fetching chat messages. The status will change to "運作中" (Running) and the chat messages will be saved to the specified file.

4. Click "停止" to stop fetching chat messages. The status will change to "停止" (Stopped).

5. To change the save file location, click "設定儲存位置" and choose a new location.

## Extracting YouTube Video ID

The application automatically extracts the video ID from the provided YouTube URL. Ensure the URL is in the correct format, such as:

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

## Example

1. Open a terminal and navigate to the directory containing `youtube-live-chat-gui.py`.
2. Run the script:

    ```bash
    python youtube-live-chat-gui.py
    ```

3. In the GUI, enter your API Key and YouTube Video URL.
4. Click "開始" to start fetching chat messages.
5. Observe the saved messages in the specified file.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google API Python Client](https://github.com/googleapis/google-api-python-client) - For providing the API client library.
- [tkinter](https://docs.python.org/3/library/tkinter.html) - For the GUI framework.

