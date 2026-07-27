
# package.json
package_json = """{
  "name": "dcn-app",
  "version": "1.0.0",
  "main": "node_modules/expo/AppEntry.js",
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web",
    "build:android": "eas build --platform android",
    "build:ios": "eas build --platform ios"
  },
  "dependencies": {
    "expo": "~51.0.0",
    "expo-status-bar": "~1.12.0",
    "expo-location": "~17.0.0",
    "expo-av": "~14.0.0",
    "expo-notifications": "~0.28.0",
    "expo-background-fetch": "~12.0.0",
    "expo-task-manager": "~11.8.0",
    "expo-battery": "~8.0.0",
    "expo-network": "~6.0.0",
    "expo-sms": "~12.0.0",
    "expo-contacts": "~13.0.0",
    "react": "18.2.0",
    "react-native": "0.74.0",
    "react-native-maps": "1.14.0",
    "react-native-ble-plx": "^3.2.1",
    "react-native-wifi-p2p": "^3.6.0",
    "react-native-async-storage": "^0.0.1",
    "@react-native-async-storage/async-storage": "1.23.1",
    "@react-navigation/native": "^6.1.17",
    "@react-navigation/bottom-tabs": "^6.5.20",
    "@react-navigation/stack": "^6.3.29",
    "@react-navigation/native-stack": "^6.9.26",
    "react-native-screens": "~3.31.0",
    "react-native-safe-area-context": "~4.10.0",
    "react-native-gesture-handler": "~2.16.0",
    "react-native-reanimated": "~3.10.0",
    "react-native-vector-icons": "^10.1.0",
    "react-native-linear-gradient": "^2.8.3",
    "react-native-shake": "^6.0.0",
    "react-native-sound": "^0.11.2",
    "react-native-vibration": "^0.0.1",
    "react-native-background-timer": "^2.4.1",
    "react-native-device-info": "^11.1.0",
    "react-native-share": "^10.2.0",
    "zustand": "^4.5.2",
    "axios": "^1.7.2",
    "socket.io-client": "^4.7.5",
    "date-fns": "^3.6.0",
    "lodash": "^4.17.21",
    "uuid": "^9.0.1"
  },
  "devDependencies": {
    "@babel/core": "^7.24.0",
    "@types/react": "~18.2.79",
    "@types/react-native": "~0.73.0",
    "typescript": "~5.3.3"
  },
  "private": true
}"""

with open(f'{app_dir}/package.json', 'w') as f:
    f.write(package_json)

print("package.json created")
