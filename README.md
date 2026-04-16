# Jomir Tathya

Jomir Tathya is a professional desktop application designed to streamline the process of looking up land property information. Built with Python and a modern UI framework, it provides an intuitive interface for searching Khatian and Plot details.

## Features

- **Secure Authentication**: Integrated login system featuring Captcha verification and OTP (One-Time Password) support for secure access.
- **Property Lookup**: Search for property details by Khatian or Plot number across various districts, blocks, and mouzas.
- **Interactive UI**: A modern, macOS-inspired interface built with `CustomTkinter` for a clean user experience.
- **Rich Data Rendering**: Displays search results using an embedded HTML viewer with Bootstrap styling.
- **Export & Print**: Capability to open search results in a dedicated browser viewer or save them directly as PDF files using `pywebview`.
- **Responsive Performance**: Utilizes multi-threading for API calls and multi-processing for document viewing to ensure the UI remains responsive during background tasks.

## Technical Stack

- **Language**: Python 3.x
- **GUI Framework**: CustomTkinter
- **Networking**: `requests` with custom SSL adapters for legacy renegotiation support.
- **HTML Rendering**: `tkinterweb` for inline results and `pywebview` for external viewing/printing.
- **State Management**: Centralized application state via an `AppState` listener pattern.
- **Image Processing**: `Pillow` (PIL) for handling logos and dynamic Captcha rendering.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd jomir-tathya
   ```

2. **Install Dependencies**:
   Ensure you have the required packages installed:
   ```bash
   pip install customtkinter requests pillow pywebview tkinterweb urllib3
   ```

## Project Structure

- `src/ui/`: Contains the screen definitions (`AppScreen`, `LoginScreen`, `PropertyScreen`).
- `src/services/`: Network and session management logic.
- `src/api/`: API wrapper functions for fetching district, block, mouza, and property data.
- `src/store/`: Global application state management.

## Usage

1. Launch the application by running the main entry point (e.g., `python main.py`).
2. Click the **Login** button to authenticate.
3. Once logged in, click on **Know Your Property**.
4. Select the desired **District**, **Block**, and **Mouza** from the dropdown menus.
5. Enter the **Khatian** or **Plot** number and click **Search**.
6. Results will appear in the right-hand panel. You can then use the **Open in Browser** or **Save as PDF** buttons to export the data.

## License

This project is developed for informational purposes. Please ensure compliance with official data usage policies.
