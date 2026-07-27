
# App.tsx - Main entry point
app_tsx = """import React, { useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { StyleSheet } from 'react-native';
import * as Notifications from 'expo-notifications';
import * as Location from 'expo-location';
import * as TaskManager from 'expo-task-manager';
import * as BackgroundFetch from 'expo-background-fetch';

import RootNavigator from './src/navigation/RootNavigator';
import { useAuthStore } from './src/store/authStore';
import { useSOSStore } from './src/store/sosStore';
import { MeshNetworkService } from './src/services/meshNetwork';
import { SOS_BACKGROUND_TASK } from './src/services/backgroundTasks';

// Configure notifications
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

// Background task for SOS monitoring
TaskManager.defineTask(SOS_BACKGROUND_TASK, async ({ data, error }) => {
  if (error) return;
  const meshService = MeshNetworkService.getInstance();
  await meshService.scanForDistressSignals();
});

export default function App() {
  const { checkAuth } = useAuthStore();
  const { initializeSOS } = useSOSStore();

  useEffect(() => {
    // Initialize auth state
    checkAuth();
    
    // Initialize SOS system
    initializeSOS();
    
    // Request permissions
    requestPermissions();
    
    // Initialize mesh network
    const meshService = MeshNetworkService.getInstance();
    meshService.initialize();
    
    // Register background task
    registerBackgroundTask();
    
    return () => {
      meshService.cleanup();
    };
  }, []);

  const requestPermissions = async () => {
    await Location.requestForegroundPermissionsAsync();
    await Location.requestBackgroundPermissionsAsync();
    await Notifications.requestPermissionsAsync();
  };

  const registerBackgroundTask = async () => {
    try {
      await BackgroundFetch.registerTaskAsync(SOS_BACKGROUND_TASK, {
        minimumInterval: 60, // 1 minute
        stopOnTerminate: false,
        startOnBoot: true,
      });
    } catch (err) {
      console.log('Background task registration failed:', err);
    }
  };

  return (
    <GestureHandlerRootView style={styles.container}>
      <SafeAreaProvider>
        <NavigationContainer>
          <RootNavigator />
          <StatusBar style="light" />
        </NavigationContainer>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
"""

with open(f'{app_dir}/App.tsx', 'w') as f:
    f.write(app_tsx)

print("App.tsx created")
