
# Check and Report Status Script

This script checks the status of all devices in all fabrics managed by NDFC (Network Device Fabric Controller). If a device is not in sync, it sends a message to a specified Webex Teams Room.

## Prerequisites

- Python 3.x
- Required Python packages:
    - `webexteamssdk`
    - `logging`

## Installation

1. Clone the repository or download the script file.
2. Install the required Python packages using pip:
    ```sh
    pip install webexteamssdk
    ```

## Configuration

1. Set the following environment variables:
    - `WEBEX_TEAMS_ACCESS_TOKEN`: Your Webex Teams access token.
    - `WEBEX_TEAMS_ROOM_ID`: The ID of the Webex Teams room where messages will be sent.

2. Update the `api_key` and `username` in the script with your NDFC API key and username.

## Usage

Run the script using Python:
    ```sh
    python3 check_and_report_status.py
    ```