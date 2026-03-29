# Arohan - Emergency Response App for the Elderly

Arohan is a mobile application designed to provide immediate assistance to elderly individuals during medical emergencies. Built with **React Native** and **Expo**, it focuses on speed, accessibility, and reliability, ensuring that help is just a tap away.

## 🚀 Key Features

*   **🚨 One-Tap SOS**: A prominent SOS button for instant emergency activation.
*   **🚑 Emergency Assist**: Quick access to call an ambulance and notify pre-configured emergency contacts.
*   **🗣️ AI Voice Guidance**: Real-time, voice-guided instructions for emergency procedures (e.g., CPR) powered by `expo-speech`.
*   **📍 Location Sharing**: Automatically shares the user's current location with responders and family members using `expo-location`.
*   **🌍 Multi-Language Support**: Fully localized interface supporting English, Hindi, Kannada, Telugu, Tamil, and Malayalam via `i18next`.
*   **⌚ Wearable Integration**: Includes a mock setup flow for pairing with health monitoring wearables.
*   **📱 Responsive Design**: Optimized UI for various screen sizes, ensuring readability and ease of use for elderly users.

## 🛠️ Tech Stack

*   **Framework**: [React Native](https://reactnative.dev/) with [Expo](https://expo.dev/)
*   **Navigation**: [Expo Router](https://docs.expo.dev/router/introduction/)
*   **State Management**: [Zustand](https://github.com/pmndrs/zustand)
*   **Maps**: [react-native-maps](https://github.com/react-native-maps/react-native-maps)
*   **Internationalization**: [i18next](https://www.i18next.com/) & [react-i18next](https://react.i18next.com/)
*   **Audio/Haptics**: `expo-av`, `expo-speech`, `expo-haptics`
*   **Language**: TypeScript

## 📂 Project Structure

The project follows the Expo Router file-based routing convention:

```
Arohan/
├── app/                 # Main application screens and routing
│   ├── emergency/       # Emergency assistance flows
│   ├── home/            # Home screen with SOS button
│   ├── i18n/            # Localization configuration and translation files
│   ├── setup/           # User setup (Profile, Emergency Contacts, Wearable)
│   ├── _layout.tsx      # Root layout configuration
│   └── index.tsx        # Entry point (often redirects/handles auth)
├── components/          # Reusable UI components
├── constants/           # App constants (Colors, Theme, Responsive Utils)
├── store/               # Zustand state stores
├── assets/              # Images, fonts, and other static assets
└── ...
```

## 🏁 Getting Started

### Prerequisites

*   [Node.js](https://nodejs.org/) (Project uses Node v20+ recommended)
*   [Expo Go](https://expo.dev/client) app on your physical device or an Android/iOS emulator.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Arohan
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npx expo start
    ```

4.  **Run on device/emulator:**
    *   **Physical Device**: Scan the QR code with the Expo Go app (camera on iOS, Expo Go on Android).
    *   **Emulator**: Press `a` for Android or `i` for iOS in the terminal.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
