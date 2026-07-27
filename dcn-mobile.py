
# Let me create a simplified, working package.json that's compatible with most Node versions
# and doesn't rely on Expo SDK 51 which requires specific Node versions

simplified_package = """{
  "name": "dcn-mobile-app",
  "version": "1.0.0",
  "main": "node_modules/expo/AppEntry.js",
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web"
  },
  "dependencies": {
    "expo": "~49.0.0",
    "expo-status-bar": "~1.6.0",
    "expo-location": "~16.1.0",
    "expo-notifications": "~0.20.1",
    "react": "18.2.0",
    "react-native": "0.72.6",
    "@react-navigation/native": "^6.1.9",
    "@react-navigation/bottom-tabs": "^6.5.11",
    "@react-navigation/native-stack": "^6.9.17",
    "react-native-screens": "~3.22.0",
    "react-native-safe-area-context": "~4.6.3",
    "react-native-gesture-handler": "~2.12.0",
    "react-native-reanimated": "~3.3.0",
    "@expo/vector-icons": "^13.0.0",
    "expo-linear-gradient": "~12.3.0",
    "@react-native-async-storage/async-storage": "1.19.3",
    "zustand": "^4.4.0",
    "axios": "^1.6.0",
    "uuid": "^9.0.0"
  },
  "devDependencies": {
    "@babel/core": "^7.20.0",
    "@types/react": "~18.2.14",
    "typescript": "^5.1.3"
  },
  "private": true
}"""

with open('/mnt/agents/output/dcn-app/package.json', 'w') as f:
    f.write(simplified_package)

print("Updated package.json with Expo 49 (more compatible)")
