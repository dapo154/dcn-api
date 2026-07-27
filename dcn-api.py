
# Also need to fix imports in App.tsx to use Expo 49 compatible imports
# and remove the background task imports that require newer Expo

app_tsx_fixed = """import React, { useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { StyleSheet } from 'react-native';

import RootNavigator from './src/navigation/RootNavigator';
import { useAuthStore } from './src/store/authStore';
import { useSOSStore } from './src/store/sosStore';
import { MeshNetworkService } from './src/services/meshNetwork';

export default function App() {
  const { checkAuth } = useAuthStore();
  const { initializeSOS } = useSOSStore();

  useEffect(() => {
    checkAuth();
    initializeSOS();
    
    const meshService = MeshNetworkService.getInstance();
    meshService.initialize();
    
    return () => {
      meshService.cleanup();
    };
  }, []);

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

with open('/mnt/agents/output/dcn-app/App.tsx', 'w') as f:
    f.write(app_tsx_fixed)

# Remove the backgroundTasks file since Expo 49 handles it differently
import os
bg_tasks_path = '/mnt/agents/output/dcn-app/src/services/backgroundTasks.ts'
if os.path.exists(bg_tasks_path):
    os.remove(bg_tasks_path)
    print("Removed backgroundTasks.ts (Expo 49 compatible)")

# Also fix the meshNetwork to remove the background task reference
mesh_fixed = """import { EventEmitter } from 'events';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface MeshNode {
  id: string;
  deviceId: string;
  lastSeen: number;
  signalStrength: number;
  hops: number;
}

interface DistressSignal {
  id: string;
  senderId: string;
  location: { latitude: number; longitude: number };
  timestamp: number;
  message: string;
  hopCount: number;
  relayPath: string[];
}

export class MeshNetworkService extends EventEmitter {
  private static instance: MeshNetworkService;
  private isInitialized: boolean = false;
  private nearbyNodes: Map<string, MeshNode> = new Map();
  private distressCache: Map<string, DistressSignal> = new Map();
  private deviceId: string = '';
  private scanInterval: any = null;

  static getInstance(): MeshNetworkService {
    if (!MeshNetworkService.instance) {
      MeshNetworkService.instance = new MeshNetworkService();
    }
    return MeshNetworkService.instance;
  }

  async initialize() {
    if (this.isInitialized) return;
    
    let storedId = await AsyncStorage.getItem('meshDeviceId');
    if (!storedId) {
      storedId = `dcn_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      await AsyncStorage.setItem('meshDeviceId', storedId);
    }
    this.deviceId = storedId;

    this.startScanning();
    this.isInitialized = true;
    console.log('Mesh network initialized:', this.deviceId);
  }

  private startScanning() {
    this.scanInterval = setInterval(async () => {
      await this.discoverPeers();
    }, 30000);
  }

  private async discoverPeers() {
    const mockPeers: MeshNode[] = [
      {
        id: 'peer_001',
        deviceId: 'dcn_device_001',
        lastSeen: Date.now(),
        signalStrength: -65,
        hops: 1,
      },
      {
        id: 'peer_002', 
        deviceId: 'dcn_device_002',
        lastSeen: Date.now(),
        signalStrength: -78,
        hops: 2,
      },
    ];

    mockPeers.forEach(peer => {
      this.nearbyNodes.set(peer.id, peer);
    });

    this.emit('peersUpdated', Array.from(this.nearbyNodes.values()));
  }

  async broadcastDistress(location: { latitude: number; longitude: number }, message: string): Promise<number> {
    const signal: DistressSignal = {
      id: `distress_${Date.now()}`,
      senderId: this.deviceId,
      location,
      timestamp: Date.now(),
      message,
      hopCount: 0,
      relayPath: [this.deviceId],
    };

    this.distressCache.set(signal.id, signal);
    await this.persistDistressSignal(signal);

    let relayCount = 0;
    for (const [peerId, node] of this.nearbyNodes) {
      if (node.hops <= 3) {
        try {
          await this.relayToPeer(peerId, signal);
          relayCount++;
        } catch (err) {
          console.error(`Failed to relay to ${peerId}:`, err);
        }
      }
    }

    this.emit('distressBroadcast', { signal, relayCount });
    return relayCount;
  }

  private async relayToPeer(peerId: string, signal: DistressSignal): Promise<void> {
    const relayedSignal = {
      ...signal,
      hopCount: signal.hopCount + 1,
      relayPath: [...signal.relayPath, this.deviceId],
    };
    console.log(`Relaying distress to ${peerId}:`, relayedSignal);
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  async scanForDistressSignals(): Promise<DistressSignal[]> {
    const stored = await AsyncStorage.getItem('meshDistressSignals');
    const signals: DistressSignal[] = stored ? JSON.parse(stored) : [];
    const activeSignals = signals.filter(s => Date.now() - s.timestamp < 3600000);
    if (activeSignals.length > 0) {
      this.emit('distressReceived', activeSignals);
    }
    return activeSignals;
  }

  async acknowledgeDistress(signalId: string): Promise<void> {
    const signal = this.distressCache.get(signalId);
    if (signal) {
      signal.relayPath.push('ACK');
      await this.persistDistressSignal(signal);
    }
  }

  getNearbyNodes(): MeshNode[] {
    return Array.from(this.nearbyNodes.values());
  }

  isMeshAvailable(): boolean {
    return this.nearbyNodes.size > 0;
  }

  private async persistDistressSignal(signal: DistressSignal): Promise<void> {
    const stored = await AsyncStorage.getItem('meshDistressSignals');
    const signals: DistressSignal[] = stored ? JSON.parse(stored) : [];
    const existingIndex = signals.findIndex(s => s.id === signal.id);
    if (existingIndex >= 0) {
      signals[existingIndex] = signal;
    } else {
      signals.push(signal);
    }
    if (signals.length > 50) signals.shift();
    await AsyncStorage.setItem('meshDistressSignals', JSON.stringify(signals));
  }

  cleanup() {
    if (this.scanInterval) {
      clearInterval(this.scanInterval);
    }
    this.nearbyNodes.clear();
    this.distressCache.clear();
  }
}
"""

with open('/mnt/agents/output/dcn-app/src/services/meshNetwork.ts', 'w') as f:
    f.write(mesh_fixed)

# Recreate the ZIP with fixed files
import shutil
shutil.make_archive('/mnt/agents/output/dcn-app-fixed', 'zip', '/mnt/agents/output/dcn-app')

print("Fixed app created with Expo 49 compatibility")
print(f"New ZIP size: {os.path.getsize('/mnt/agents/output/dcn-app-fixed.zip') / 1024:.1f} KB")
